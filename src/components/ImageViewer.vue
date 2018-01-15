<template>
  <div id="root">
    <div id="imageViewer">
    </div>
  </div>
</template>


<script>
  /* eslint-disable global-require */

  import OpenSeadragon from 'openseadragon';
  import dataset from '../../static/dataset/dataset.json';
  import EventBus from '../event-bus';

  export default {
    name: 'ImageViewer',
    mounted: () => {
      // eslint-disable-next-line
      const viewer = OpenSeadragon({
        id: 'imageViewer',
        showNavigationControl: false,
        gestureSettingsMouse: {
          clickToZoom: false,
        },
        viewportMargins: { top: 10, left: 10, right: 10, bottom: 10 },
      });

      let offset = 0;
      Object.keys(dataset.images).forEach((key) => {
        const image = dataset.images[key];
        viewer.addSimpleImage({
          x: offset,
          height: 1,
          // eslint-disable-next-line import/no-dynamic-require
          url: `/static/dataset/${image.file}`,
          success: (event) => {
            const tiledImage = event.item;

            Object.values(image.overlays).forEach((overlay) => {
              const elem = document.createElement('div');
              elem.id = `image-${overlay.id}`;
              elem.className = 'bla';
              elem.title = overlay.id;
              elem.onclick = () => {
                EventBus.$emit('audio_seek', dataset.alignment[overlay.id]);
              };

              const rect = tiledImage.imageToViewportRectangle(
                overlay.x,
                overlay.y,
                overlay.width,
                overlay.height,
              );

              viewer.addOverlay({
                element: elem,
                location: rect,
                placement: OpenSeadragon.Placement.TOP_LEFT,
              });
            });
          },
        });
        offset += 0.85;
      });
    },
  };
</script>


<style>
  #root, #imageViewer {
    width: 100%;
    height: 100%;
  }

  .bla {
    background-color: #00666640;
    outline: #006666f0 solid 2px;

  }

</style>
