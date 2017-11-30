<template>
  <div>
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
  // import MinimapPlugin from 'wavesurfer.js/dist/plugin/wavesurfer.minimap.min';

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
          }),
          // MinimapPlugin.create({
          //   container: '#waveform-minimap',
          // }),
        ],
      });
      this.wavesurfer.load('https://ia902606.us.archive.org/35/items/shortpoetry_047_librivox/song_cjrg_teasdale_64kb.mp3');
      this.$refs.wrapper.addEventListener('wheel', this.zoom);
      this.$parent.$on('resize', this.redraw);
      // eslint-disable-next-line no-console
      console.log(this.$parent);
    },
    data() {
      return {
        zoomLevel: 0,
      };
    },
    methods: {
      play() {
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

        console.log(this.wavesurfer);
        this.wavesurfer.drawer.height = this.$parent.container.height;
        this.wavesurfer.drawBuffer();
        // this.wavesurfer.minimap.render();
      },
    },
  };
</script>

<style scoped>

</style>

<!--TODO:-->
<!--Generate Loudness Audio files:-->
<!--https://github.com/bbc/audiowaveform/blob/master/doc/DataFormat.md-->
