tinymce.init({
    selector: 'textarea',
    height: 500,
    theme: 'modern',
    plugins: 'print preview fullpage powerpaste searchreplace autolink directionality advcode visualblocks visualchars fullscreen image link media template codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists textcolor wordcount tinymcespellchecker a11ychecker imagetools mediaembed  linkchecker contextmenu colorpicker textpattern help',
    toolbar1: 'formatselect | bold italic strikethrough forecolor backcolor | link | alignleft aligncenter alignright alignjustify  | numlist bullist outdent indent  | removeformat',
    image_advtab: true,
    templates: [
        {title: 'code', content: `
            <code style="color: black">code here</code>
        `},
        {title: 'keyboard', content: `
            <kbd style="color: black">Ctrl + S</kbd>
        `},
        {title: 'samp', content: `
            <samp style="color: black">Error!</samp>
        `},
        {title: 'terminal', content: `
            <pre style="display: block;
                        padding: 9.5px;
                        margin: 0 0 10px;
                        font-size: 13px;
                        line-height: 1.42857;
                        background-color: #f5f7fa;
                        border: 1px solid #EEF1F6;
                        border-radius: 4px;
                        word-wrap: normal;
                        word-break: normal;
                        color: #596981;
                        ">$ sudo ...</pre>
        `},
    ],
    content_css: [
        '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
        '//www.tinymce.com/css/codepen.min.css'
    ]
});

function clear() {
    $('.mce-close').click();
}

setTimeout(clear, 1000);
setTimeout(clear, 2000);
setTimeout(clear, 3000);