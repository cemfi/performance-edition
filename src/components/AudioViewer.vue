<template>
  <div id="container">
    <div id="waveform-minimap"></div>
    <div ref="wrapper">
      <div ref="waveform" id="waveform" @scroll="zoom"></div>
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

  import dataset from '../../static/dataset/dataset.json';

  const TIMELINE_HEIGHT = 20;

  export default {
    name: 'AudioViewer',
    destroy() {

    },
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
      this.wavesurfer.load('/static/dataset/Curzon_original.mp3');
      this.$refs.wrapper.addEventListener('wheel', this.zoom);
      this.wavesurfer.drawer.wrapper.addEventListener('scroll', this.redraw);
      this.$parent.$on('resize', this.redraw);
      EventBus.$on('playPause', this.playPause);
      EventBus.$on('jumpToMeasure', this.jumpToMeasure);
      EventBus.$on('jumpToSecond', this.setCurrentTime);
    },
    data() {
      return {
        zoomLevel: 0,
      };
    },
    methods: {
      playPause() {
        console.log('playPause');
        this.wavesurfer.playPause();
      },
      jumpToMeasure(measure) {
        this.setCurrentTime(dataset.alignment[measure]);
      },
      setCurrentTime(secs) {
        this.wavesurfer.seekTo(secs / this.wavesurfer.getDuration());
      },
      zoom(event) {
        let zoomLevel = this.$data.zoomLevel;
        zoomLevel -= Math.sign(event.deltaY) * 6;
        if (zoomLevel < 0) {
          zoomLevel = 0;
        } else if (zoomLevel > 80) {
          zoomLevel = 80;
        }
        if (this.$data.zoomLevel !== zoomLevel) {
          this.$data.zoomLevel = zoomLevel;
          this.wavesurfer.zoom(zoomLevel);
          this.redraw();

          // eslint-disable-next-line no-console
          console.log(this.$data.zoomLevel);
          // eslint-disable-next-line no-console
          console.log(this.wavesurfer);
        }
      },
      redraw() {
        const newHeight = (this.$parent.container.height - TIMELINE_HEIGHT - (this.$el.offsetTop * 2));
        const waveform = this.$refs.waveform.getElementsByTagName('wave')[0];
        waveform.style.height = `${newHeight}px`;
        // this.wavesurfer.params.height = newHeight;
        // this.wavesurfer.drawer.setHeight(newHeight);
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

  /*wave {*/
  /*height: 100%;*/
  /*}*/

</style>

<!--TODO:-->
<!--Generate Loudness Audio files:-->
<!--https://github.com/bbc/audiowaveform/blob/master/doc/DataFormat.md-->
