<template>
  <layout-golden class="screen" :showPopoutIcon="false" :showCloseIcon="false" :showMaximiseIcon="false">
    <!--<layout-golden class="screen" >-->
    <gl-row>
      <!--<gl-col :width="0.2">-->
        <!--<gl-component title="Annotationen" :closable="false">-->
          <!--<AnnotationViewer></AnnotationViewer>-->
        <!--</gl-component>-->
      <!--</gl-col>-->

      <gl-col :width="0.8">
        <gl-component title="Aufnahme" :height="0.2" :closable="false">
          <AudioViewer></AudioViewer>
        </gl-component>
        <gl-row :height="0.8">
          <gl-component title="Quellnoten" :closable="false">
            <ImageViewer></ImageViewer>
          </gl-component>
          <gl-component title="MEI-Rendering" :closable="false">
            <VerovioViewer></VerovioViewer>
          </gl-component>
        </gl-row>
      </gl-col>
    </gl-row>
  </layout-golden>
</template>

<script>
  import AudioViewer from './AudioViewer';
  import ImageViewer from './ImageViewer';
  import VerovioViewer from './VerovioViewer';
  import AnnotationViewer from './AnnotationViewer';

  export default {
    name: 'Navigator',
    components: {
      AudioViewer,
      ImageViewer,
      VerovioViewer,
      AnnotationViewer,
    },
  };
</script>

<style scoped>
  .screen {
    width: 100%;
    height: 100%;
  }
</style>
