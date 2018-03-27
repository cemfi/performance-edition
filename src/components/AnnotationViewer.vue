<template>
  <div id="annotations">{{annotation.text}}</div>

</template>

<script>
  import EventBus from '../event-bus';

  export default {
    name: 'AnnotationViewer',
    mounted() {
      EventBus.$on('openAnnotation', this.openAnnotation);
    },
    methods: {
      openAnnotation(annotation) {
        this.$data.annotation = annotation;
      },
    },
    data() {
      return {
        annotation: {},
      };
    },
  };
</script>

<style scoped>
  #annotations {
    padding: 10px;
    text-align: left;
    /*background-color: #ffffff;*/
  }
</style>
