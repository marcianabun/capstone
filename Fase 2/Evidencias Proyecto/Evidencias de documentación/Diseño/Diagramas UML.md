# Diagramas UML

Diagramas de **clases**, **secuencia** y **componentes** del sistema, hechos desde el código real (`src/`, `web/`) al 2026-11-16. Están en Mermaid: GitHub los dibuja en esta misma página. Imágenes (con su fuente en `Diagramas fuente (Mermaid)/`): [clases](Diagrama%20de%20Clases.png), [secuencia](Diagrama%20de%20Secuencia%20-%20Analisis%20de%20una%20foto.png) y [componentes](Diagrama%20de%20Componentes.png). Se generan con el comando de `Diagramas fuente (Mermaid)/LEEME.md`. Los diagramas de casos de uso están en [Diagrama General Casos de Uso.png](Diagrama%20General%20Casos%20de%20Uso.png) y en `Diagramas particulares por cada C. U._/`; la arquitectura, en [Diagrama de Arquitectura.png](Diagrama%20de%20arquitectura/Diagrama%20de%20Arquitectura.png).

## 1. Diagrama de clases

Las estructuras del pipeline son `dataclass` inmutables que las etapas se pasan entre sí (regla "pipeline modular" de `CLAUDE.md`); los modelos de la aplicación web son los de Django (`web/models.py`).

```mermaid
classDiagram
    direction TB

    class CorrectedImage {
        +ndarray image
        +LensCalibration calibration
        +to_original_points(points)
    }
    class GondolaSegmentation {
        +PixelBBox roi
        +ShelfLine[] shelf_lines
        +PixelBBox[] shelves
        +bool found
    }
    class RoiCrop {
        +ndarray image
        +PixelBBox roi
        +to_original(bbox) BBox
    }
    class Detection {
        +BBox bbox
        +float score
        +int class_id
        +str class_name
    }
    class ProductDetector {
        +detect(image, conf) Detection[]
    }
    class GondolaAvailability {
        +ShelfAvailability[] shelves
        +float free_fraction
        +bool critical
        +float occluded_fraction
        +bool inconclusive
    }
    class PipelineResult {
        +tuple image_size
        +BBox roi
        +BBox[] products
        +ShelfResult[] shelves
        +float free_fraction
        +bool critical
        +bool segmentation_found
        +float occluded_fraction
        +bool inconclusive
        +StageTimes times
        +to_dict() dict
    }

    class User {
        +str email
        +int failed_logins
        +datetime locked_until
        +role() str
    }
    class Analysis {
        +datetime created_at
        +str pasillo
        +str gondola
        +str photo_name
        +float free_fraction
        +bool critical
        +JSON result
        +File annotated
        +str estado
        +datetime estado_at
    }
    class Config {
        +int umbral
    }
    class Camera {
        +str nombre
        +str pasillo
        +str gondola
        +JSON calibracion
    }

    CorrectedImage ..> GondolaSegmentation : segment_gondola()
    GondolaSegmentation ..> RoiCrop : crop_roi()
    ProductDetector ..> Detection : produce
    RoiCrop ..> ProductDetector : imagen recortada
    Detection ..> GondolaAvailability : compute_availability()
    GondolaAvailability ..> PipelineResult : informa
    PipelineResult ..> Analysis : to_dict() en result
    User "1" --> "*" Analysis : created_by
    User "0..1" --> "*" Analysis : taken_by
    Config ..> PipelineResult : umbral de alerta
    Camera ..> CorrectedImage : calibración de lente
```

## 2. Diagrama de secuencia: análisis de una foto (CU01 y CU02)

```mermaid
sequenceDiagram
    actor U as Reponedor o Jefe de Salón
    participant W as App web (views.analyze)
    participant P as pipeline.run_image
    participant C as preprocessing
    participant D as ProductDetector (YOLO26)
    participant O as PersonDetector (YOLO26 de COCO)
    participant A as postprocessing
    participant DB as Base de datos (SQLite)

    U->>W: Sube la foto (JPG o PNG, hasta 20 MB), pasillo y góndola
    W->>W: Valida la foto y lee umbral (Config) y calibración (Camera)
    W->>P: run_image(imagen, detector, calibración, umbral)
    P->>C: correct_image() (dewarping y CLAHE)
    C-->>P: CorrectedImage
    P->>C: segment_gondola() y crop_roi()
    C-->>P: GondolaSegmentation y RoiCrop
    P->>D: detect(recorte)
    D-->>P: Detection[]
    P->>O: detect(imagen corregida)
    O-->>P: personas que tapan la góndola
    P->>P: RoiCrop.to_original() y CorrectedImage.to_original()
    P->>A: shelf_levels() y compute_availability(occluders)
    A-->>P: free_fraction, critical e inconclusive (lo tapado no cuenta)
    P-->>W: PipelineResult
    alt Sin productos detectados o góndola tapada en más de la mitad
        W-->>U: Rechaza la foto, sin alerta (no toca la alerta abierta)
    else Hay productos
        W->>DB: Cierra la alerta anterior, guarda la foto anotada y crea el Analysis (una transacción)
        W-->>U: Resultado: % libre y alerta si libre >= umbral
    end
```

## 3. Diagrama de componentes

```mermaid
flowchart LR
    subgraph Cliente
        NAV[Navegador web]
    end

    subgraph Docker["Contenedor Docker (docker-compose.yml)"]
        subgraph WEB["web/ (Django 6.1 y gunicorn)"]
            VIS[Vistas, formularios y plantillas]
            MOD[Modelos: User, Analysis, Config, Camera]
        end
        subgraph PIPE["src/ (pipeline)"]
            PRE["preprocessing/ (OpenCV)"]
            MDL["models/ (YOLO26 Ultralytics: productos y personas)"]
            POST["postprocessing/ (disponibilidad y alerta)"]
            REP["reporting/ (vista anotada, Excel, CSV y PDF)"]
            RUN[pipeline.py: run_image]
        end
        W[("weights/: yolo26s-finetune-ruido-v3.pt y yolo26n.pt (en la imagen)")]
        VOL[("Volumen /data: SQLite y fotos")]
    end

    NAV -->|HTTPS| VIS
    VIS --> MOD
    VIS -->|run_image| RUN
    RUN --> PRE --> MDL --> POST --> REP
    MOD --> VOL
    MDL -->|pesos| W
    VIS -->|reportes| REP

    CI[GitHub Actions: pytest y docker build] -.->|valida| Docker
```
