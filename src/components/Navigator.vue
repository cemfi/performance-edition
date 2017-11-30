<template>
  <layout-golden class="screen" :showPopoutIcon="false" :showCloseIcon="false" :showMaximiseIcon="false">
    <gl-row>
      <gl-col :width="0.8">
        <gl-component title="Aufnahme" :height="0.15" :closable="false">
          <Waveform></Waveform>
        </gl-component>
        <gl-row :height="0.85">
          <gl-component v-for="key in activeSources" :key="key" :title="sources[key].name"></gl-component>
        </gl-row>
      </gl-col>
      <gl-col :width="0.2">
        <gl-component title="Notenquellen" :height="0.3" :closable="false">
          <div v-for="(source, key) in sources">
            <input type="checkbox"
                   :id="key"
                   :name="source.name"
                   :value="key"
                   v-model="activeSources">
            {{ source.name }}
          </div>
        </gl-component>
        <gl-component title="Details" :height="0.5" :closable="false"></gl-component>
      </gl-col>
    </gl-row>
  </layout-golden>
</template>

<script>
  import Waveform from './Waveform';

  export default {
    name: 'Navigator',
    components: {
      Waveform,
    },
    data() {
      return {
        sources: {
          a: {
            name: 'Quelle A',
          },
          b: {
            name: 'Quelle B',
          },
        },
        activeSources: [],
      };
    },
    created() {
      Object.keys(this.sources).forEach((key) => {
        this.activeSources.push(key);
      });
    },
  };
</script>

<style scoped>
  .screen {
    width: 100%;
    height: 100%;
  }
</style>
