let loading = document.getElementById("loading").innerHTML;
document.getElementById("search-btn").onclick = function () {
    let search_text = document.getElementById("search-input").value;
    $.ajax({
        url: "{% url 'blog:dashboard:search-post' %}",
        method: "GET",
        data: {
            'text_search': search_text
        },
        dataType: 'json',
        beforeSend: function () {
            document.getElementById("loading").innerHTML = loading;
            document.getElementById("loading").removeAttribute("hidden");
        },
        success: function (data) {
            if (data.length === 0) {
                document.getElementById("loading").innerHTML =
                    `<div class="col align-self-center text-center">
                                    <div class="alert alert-primary">
                                        <i class="la la-search"></i> Không tìm thấy bài viết có liên quan
                                    </div>
                                </div>`;

                return;
            }
            let content = String();
            data.forEach(e => {
                content += '<li class="list-group-item">\n' +
                    '                          <h3 class="name">' + '<a href="edit-article/' + e.slug + '">' + e.title + '</a>' + '</h3>\n' +
                    '                          <p class="born">' + e.publish_date + '</p></li>\n';
            });
            document.getElementById("loading").innerHTML = '<div class="col align-self-center text-center"><ul class="list-group list">' + content + '</ul></div>';
        }
    })
};

$('.quick-view').bind('click', function () {
    article_id = $(this).attr('data-value');
    $.ajax({
        url: '{% url "blog:dashboard:get-content-quick-view"  %}',
        method: 'GET',
        data: {
            'uuid': article_id
        },
        dataType: 'json',
        success: function (data, status) {
            $title = $('#quick-view-title');
            if (data.length === 0) {
                $title.text(status);
                return;
            }
            $title.text(data.title);
            $('#content-view').load(data.content);
        }
    })
});

let is_confirmed = false;
$(".conf-modal-dialog-btn-del").on("click", function (event) {
    if (!is_confirmed) {
        event.preventDefault();
        $('.conf-modal-dialog').html("Bạn có muốn xóa <b>" + $(this).attr('data-value') + "</b>?");
        $(".conf-modal-dialog").dialog("open");
        return;
    }
    is_confirmed = false;
    location.href = $(this).attr('href');
});

$(".conf-modal-dialog").dialog({
    autoOpen: false,
    resizable: false,
    height: "auto",
    width: 400,
    draggable: false,
    modal: true,
    buttons: {
        "Xóa": function () {
            is_confirmed = true;
            $(".conf-modal-dialog-btn-del").trigger('click');
            $(this).dialog("close");
        },
        Cancel: function () {
            $(this).dialog("close");
        }
    },
});