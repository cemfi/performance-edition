<template>
  <div id="container">
    <div id="waveform-minimap"></div>
    <div ref="wrapper">
      <div id="waveform" @scroll="zoom"></div>
      <div id="waveform-timeline"></div>
    </div>
    <!--<button @click="play">Play / Pause</button>-->
  </div>
</template>


<script>
  import WaveSurfer from 'wavesurfer.js';
  import TimelinePlugin from 'wavesurfer.js/dist/plugin/wavesurfer.timeline.min';

  import EventBus from '../event-bus';
  // import MinimapPlugin from 'wavesurfer.js/dist/plugin/wavesurfer.minimap.min';

  const TIMELINE_HEIGHT = 20;

  export default {
    name: 'Waveform',
    mounted() {
      this.wavesurfer = WaveSurfer.create({
        container: '#waveform',
        waveColor: '#EEEEEE',
        progressColor: '#999999',
        normalize: true,
        plugins: [
          TimelinePlugin.create({
            container: '#waveform-timeline',
            primaryColor: '#EEEEEE',
            secondaryColor: '#666666',
            primaryFontColor: '#EEEEEE',
            secondaryFontColor: '#EEEEEE',
            height: TIMELINE_HEIGHT,
          }),
          // MinimapPlugin.create({
          //   container: '#waveform-minimap',
          // }),
        ],
      });
      // eslint-disable-next-line global-require
      this.wavesurfer.load(require('../assets/Curson_original.mp3'));

      this.$refs.wrapper.addEventListener('wheel', this.zoom);
      this.wavesurfer.drawer.wrapper.addEventListener('scroll', this.redraw);
      this.$parent.$on('resize', this.redraw);
      // EventBus.$on('resize', this.redraw);
      EventBus.$on('playPause', this.playPause);
    },
    data() {
      return {
        zoomLevel: 0,
      };
    },
    methods: {
      playPause() {
        this.wavesurfer.playPause();
      },
      zoom(event) {
        let zoomLevel = this.$data.zoomLevel;
        zoomLevel -= Math.sign(event.deltaY) * 8;
        if (zoomLevel < 0) {
          zoomLevel = 0;
        } else if (zoomLevel > 100) {
          zoomLevel = 100;
        }
        if (this.$data.zoomLevel !== zoomLevel) {
          this.$data.zoomLevel = zoomLevel;
          this.wavesurfer.zoom(zoomLevel);
          this.redraw();

          // eslint-disable-next-line no-console
          console.log(this.$data.zoomLevel);
        }
      },
      redraw() {
        const newHeight = this.$parent.container.height - TIMELINE_HEIGHT - (this.$el.offsetTop * 2);
        this.wavesurfer.params.height = newHeight;
        this.wavesurfer.drawer.setHeight(newHeight);
        try {
          this.wavesurfer.drawBuffer();
          // eslint-disable-next-line no-empty
        } catch (e) {
        }
        // this.wavesurfer.minimap.render();
      },
    },
  };
</script>

<style scoped>
  #container {
    margin: 10px;
  }

</style>

<!--TODO:-->
<!--Generate Loudness Audio files:-->
<!--https://github.com/bbc/audiowaveform/blob/master/doc/DataFormat.md-->
