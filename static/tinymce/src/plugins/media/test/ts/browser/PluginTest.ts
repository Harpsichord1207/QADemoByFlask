import { Pipeline } from '@ephox/agar';
import { TinyLoader } from '@ephox/mcagar';
import { TinyUi } from '@ephox/mcagar';
import Plugin from 'tinymce/plugins/media/Plugin';
import Utils from '../module/test/Utils';
import Theme from 'tinymce/themes/modern/Theme';
import { UnitTest } from '@ephox/bedrock';

UnitTest.asynctest('browser.tinymce.plugins.media.PluginTest', function () {
  const success = arguments[arguments.length - 2];
  const failure = arguments[arguments.length - 1];

  Plugin();
  Theme();

  TinyLoader.setup(function (editor, onSuccess, onFailure) {
    const ui = TinyUi(editor);

    Pipeline.async({}, [
      Utils.sTestEmbedContentFromUrl(ui,
        'https://www.youtube.com/watch?v=b3XFjWInBog',
        '<iframe src="//www.youtube.com/embed/b3XFjWInBog" width="560" height="314" allowFullscreen="1"></iframe>'
      ),
      Utils.sTestEmbedContentFromUrl(ui,
        'https://www.google.com',
        '<video width="300" height="150" controls="controls">\n<source src="https://www.google.com" />\n</video>'
      ),
      Utils.sAssertSizeRecalcConstrained(ui),
      Utils.sAssertSizeRecalcUnconstrained(ui),
      Utils.sAssertSizeRecalcConstrainedReopen(ui)
    ], onSuccess, onFailure);
  }, {
    plugins: ['media'],
    toolbar: 'media',
    skin_url: '/project/js/tinymce/skins/lightgray'
  }, success, failure);
});
