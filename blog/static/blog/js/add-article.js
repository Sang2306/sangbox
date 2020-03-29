$('button[type=submit]').click(function () {
    let content = tinymce.activeEditor.getContent();
    let html = tinymce.activeEditor.getDoc().documentElement.outerHTML;
    $('input[name=content]').val(content);
    $('input[name=html]').val(html);
});