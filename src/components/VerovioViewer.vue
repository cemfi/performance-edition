<template>
  <div id="root">
    <div id="verovioViewer">
    </div>
  </div>
</template>


<script>
  /* eslint-disable global-require */

  import OpenSeadragon from 'openseadragon';

  export default {
    name: 'VerovioViewer',
    mounted() {
      // eslint-disable-next-line
      const viewer = OpenSeadragon({
        id: 'verovioViewer',
        showNavigationControl: false,
        gestureSettingsMouse: {
          clickToZoom: false,
        },
        viewportMargins: { top: 10, left: 10, right: 10, bottom: 10 },
      });

      viewer.addSimpleImage({ url: '/static/dataset/output_1.svg' });
      viewer.addSimpleImage({ url: '/static/dataset/output_2.svg', x: 1.05 });

//       const options = {
// //    border: 100,
//         scale: 50,
//         pageWidth: 2100,
//         adjustPageHeight: true,
//       };
//       const vrvToolkit = new verovio.toolkit();
//       $.ajax({
//         url: '/static/dataset/aligned.mei',
//         type: 'GET',
//         crossDomain: true,
//         success: (response) => {
//           vrvToolkit.setOptions(options);
//           vrvToolkit.loadData(response);
//           vrvToolkit.redoLayout();
//           const pageCount = vrvToolkit.getPageCount();
//           // Add transparent pixel as a placeholder. SVG will be added as overlay
//           viewer.addSimpleImage({
//             url: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+ip1sAAAAASUVORK5CYII=',
//             // url: 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==',
//             height: 1,
//             success: (event) => {
//               for (let i = 1; i <= 1; i += 1) {
//                 const elem = document.createElement('div');
//                 elem.id = `verovio-${i}`;
//                 elem.className = 'verovioScore';
//                 elem.innerHTML = vrvToolkit.renderPage(i, options);
//
//                 viewer.addOverlay({
//                   element: elem,
//                   checkResize: true,
//                   location: new OpenSeadragon.Rect(),
//                   placement: OpenSeadragon.Placement.TOP_LEFT,
//                 });
//               }
//             },
//           });
//           // $('#verovioViewer').html(svg);
//         },
//       });
    },
  };
</script>


<style>
  #root, #verovioViewer {
    width: 100%;
    height: 100%;
    display: flex;
  }

  #verovioViewer {
    box-sizing: border-box;
  }

  .verovioScore {
    width: 100% !important;
    height: 100% !important;
  }

  .verovioScore svg {
    /*background-color: #ffffff;*/
  }
</style>
