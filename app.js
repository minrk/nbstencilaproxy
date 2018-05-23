(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? factory(require('substance'), require('substance-texture'), require('stencila')) :
  typeof define === 'function' && define.amd ? define(['substance', 'substance-texture', 'stencila'], factory) :
  (factory(global.window.substance,global.window.texture,global.window.stencila));
}(this, (function (substance,substanceTexture,stencila) { 'use strict';

  window.addEventListener('load', () => {
    substance.substanceGlobals.DEBUG_RENDERING = substance.platform.devtools;
    stencila.StencilaWebApp.mount({
      archiveId: substance.getQueryStringParam('archive') || '{{archive}}',
      storageType: substance.getQueryStringParam('storage') || 'fs',
      storageUrl: substance.getQueryStringParam('storageUrl') || './archives'
    }, window.document.body);
  });

})));
