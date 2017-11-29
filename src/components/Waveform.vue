<template>
  <div>
    <div id="waveform-minimap"></div>
    <div ref="wrapper">
      <div id="waveform" @scroll="zoom"></div>
      <div id="waveform-timeline"></div>
    </div>
    <button @click="play">Play / Pause</button>
  </div>
</template>


<script>
  import WaveSurfer from 'wavesurfer.js';
  import TimelinePlugin from 'wavesurfer.js/dist/plugin/wavesurfer.timeline.min';
  import MinimapPlugin from 'wavesurfer.js/dist/plugin/wavesurfer.minimap.min';

  export default {
    name: 'Waveform',
    mounted() {
      this.wavesurfer = WaveSurfer.create({
        container: '#waveform',
        waveColor: 'violet',
        plugins: [
          TimelinePlugin.create({
            container: '#waveform-timeline',
          }),
          MinimapPlugin.create({
            container: '#waveform-minimap',
          }),
        ],
      });
      this.wavesurfer.load('https://ia902606.us.archive.org/35/items/shortpoetry_047_librivox/song_cjrg_teasdale_64kb.mp3');
      this.$refs.wrapper.addEventListener('wheel', this.zoom);
    },
    destroyed() {
      this.$refs.wrapper.removeEventListener('wheel', this.zoom);
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
        // eslint-disable-next-line no-console
        console.log(this.$data.zoomLevel);
      },
    },
  };
</script>

<style scoped>

</style>
