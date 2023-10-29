import merge from '@hugojosefson/merge-html'

const { PDFNet } = require('@pdftron/pdfnet-node');

const main = async() => {
    const htmlOutputOptions = new PDFNet.Convert.HTMLOutputOptions();
    // htmlOutputOptions.setContentReflowSetting(2);
    // console.log(PDFNet.Convert.HTMLOutputOptions)
    htmlOutputOptions.setNoPageWidth(true);

    console.log(merge);

    await PDFNet.Convert.fileToHtml('./src/main.pdf', './out/pdf_better.html', htmlOutputOptions);
};


PDFNet.runWithCleanup(main, 'demo:1691866956169:7c54acf103000000009fbdd96af28219f8b9cdcc4dbd405a7921b35ca4').catch(function(error) {
  console.log('Error: ' + JSON.stringify(error));
}).then(function(){ PDFNet.shutdown(); });
