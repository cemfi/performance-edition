<template>
  <div id="root">
    <div id="verovioViewer">
    </div>
  </div>
</template>


<script>
  /* eslint-disable global-require */

  import Bla from 'openseadragon';

  export default {
    name: 'VerovioViewer',
    mounted() {
      // eslint-disable-next-line
      const viewer = Bla({
        id: 'verovioViewer',
        showNavigationControl: false,
        clickToZoom: false,
        viewportMargins: { top: 10, left: 10, right: 10, bottom: 10 },
      });
      viewer.addSimpleImage({ url: require('../dataset/output_1.svg') });
      viewer.addSimpleImage({ url: require('../dataset/output_2.svg'), x: 1.05 });
    },
  };
</script>


<style scoped>
  #root, #verovioViewer {
    width: 100%;
    height: 100%;
  }

  #verovioViewer {
    background-color: white;
  }

</style>
