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

            // Measure overlays
            Object.values(image.measures).forEach((measure) => {
              const elem = document.createElement('div');
              elem.id = `image-${measure.id}`;
              elem.className = 'measure';
              elem.title = measure.id;
              elem.onclick = () => {
                EventBus.$emit('jumpToMeasure', measure.id);
              };

              const rect = tiledImage.imageToViewportRectangle(
                measure.x,
                measure.y,
                measure.width,
                measure.height,
              );

              viewer.addOverlay({
                element: elem,
                location: rect,
                placement: OpenSeadragon.Placement.TOP_LEFT,
              });
            });

            // Annotations overlays
            Object.values(image.annotations).forEach((annotation) => {
              const elem = document.createElement('div');
              elem.id = `image-${annotation.id}`;
              elem.className = 'annotation';
              // elem.title = annotation.text;
              elem.setAttribute('data-tooltip', '');
              elem.setAttribute('data-tooltip-message', annotation.text);
              elem.onclick = () => {
                // EventBus.$emit('openAnnotation', annotation);
                EventBus.$emit('jumpToSecond', annotation.time);
              };

              const rect = tiledImage.imageToViewportRectangle(
                annotation.x,
                annotation.y,
                annotation.width,
                annotation.height,
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

  /*.measure {*/
    /*background-color: #00666610;*/
    /*outline: #00666640 solid 2px;*/
  /*}*/

  /*.measure:hover {*/
    /*background-color: #00666640;*/
    /*!*outline: #006666f0 solid 2px;*!*/
  /*}*/

  .annotation {
    background-color: #00666630;
    outline: #00666650 solid 2px;
  }

  .annotation:hover {
    background-color: #00666650;
    /*outline: #006666f0 solid 2px;*/
  }

  [data-tooltip] {
    position: relative;
  }

  [data-tooltip]:before,
  [data-tooltip]:after {
    display: none;
    position: absolute;
    top: 0;
  }

  [data-tooltip]:after {
    background-color: #006666;
    border: 4px solid #006666;
    border-radius: 7px;
    color: #ffffff;
    content: attr(data-tooltip-message);
    left: 10px;
    top: 10px;
    margin-left: 100%;
    padding: 5px 15px;
    white-space: pre-wrap;
    width: 250px;
    z-index: 1000;
  }

  [data-tooltip]:hover:after,
  [data-tooltip]:hover:before {
    display: block;
  }


</style>
