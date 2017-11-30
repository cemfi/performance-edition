<template>
  <div id="app">
    <Navigator/>
  </div>
</template>

<script>
  import Navigator from './components/Navigator';

  export default {
    name: 'app',
    components: {
      Navigator,
    },
  };
</script>

<style src="@/theme/goldenlayout.less" lang="less"></style>
<style src="@/theme/custom.less" lang="less"></style>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #ffffff;
    margin: 0;
    padding: 0;
    height: 100%;
  }
</style>
