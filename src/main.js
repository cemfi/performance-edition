// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import vgl from 'vue-golden-layout';
import vuescroll from 'vue-scroll';

import EventBus from './event-bus';

import App from './App';

Vue.use(vgl);
Vue.use(vuescroll);

Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  template: '<App/>',
  components: { App },
  mounted() {
    // Emit event for pressed spacebar to play audio file
    window.addEventListener('keypress', (event) => {
      const key = event.keyCode || event.charCode; // cross browser support
      if (key === 32) { // spacebar
        EventBus.$emit('playPause');
      }
    });
    window.addEventListener('resize', () => {
      EventBus.$emit('resize');
    });
  },
});
