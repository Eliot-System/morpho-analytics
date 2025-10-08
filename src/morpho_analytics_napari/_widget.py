"""Widget Napari pour le tracking avec morpho-analytics."""
from magicgui import magicgui
import napari
from napari.layers import Image
from napari.types import LayerDataTuple

from morpho_analytics.track import track


def tracking_widget():
    """Factory: retourne un widget MagicGUI prêt à être docké dans napari."""

    @magicgui(call_button="Run Tracking")
    def _widget(
        viewer: napari.Viewer,
        image_layer: Image,
        threshold: float = 0.5,
        connectivity: int = 4,
        min_area: int = 10,
    ) -> LayerDataTuple:
        """Exécute le tracking et retourne une couche de labels."""
        if image_layer is None:
            print("No image layer selected. Please select an image layer.")
            return

        print(f"Processing {image_layer.name}...")

        data = image_layer.data
        if data.ndim not in (2, 3):
            print(
                f"Unsupported data dimension: {data.ndim}. Expected 2D (H, W) or 3D (T, H, W)."
            )
            return

        if data.ndim == 2:
            data = data[None, :, :]

        tracks_result = track(
            data,
            threshold=threshold,
            connectivity=connectivity,
            min_area=min_area,
        )

        print("Tracking complete.")

        if isinstance(tracks_result.labels, list):
            if not tracks_result.labels:
                print("No labels produced by tracking.")
                return
            labels_to_display = tracks_result.labels[0]
        else:
            labels_to_display = tracks_result.labels

        layer_meta = {"name": f"{image_layer.name}-labels"}
        return labels_to_display, layer_meta, "labels"

    return _widget
