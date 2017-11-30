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
      this.wavesurfer.load('https://ia800508.us.archive.org/15/items/LoveThemeFromTheGodfather/02LoveThemeFromTheGodfather.mp3');

      this.$refs.wrapper.addEventListener('wheel', this.zoom);
      this.$parent.$on('resize', this.redraw);
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
        } else if (zoomLevel > 400) {
          zoomLevel = 400;
        }
        this.$data.zoomLevel = zoomLevel;
        this.wavesurfer.zoom(zoomLevel);
        this.redraw();
        // eslint-disable-next-line no-console
        console.log(this.$data.zoomLevel);
      },
      redraw() {
        const newHeight = this.$parent.container.height - TIMELINE_HEIGHT - (this.$el.offsetTop * 2);
        this.wavesurfer.params.height = newHeight;
        this.wavesurfer.drawer.setHeight(newHeight);
        this.wavesurfer.drawBuffer();
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
