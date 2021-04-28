$(document).ready(function(){
    $("#comment").on('click', function(event){
        event.preventDefault();
        var post = $("#like_post").val()
        var user = $("#like_post").attr('name')
        var comments_tag = $('#comments')
        var form = $("#form-me")
        form.toggleClass('d-none ')
        comments_tag.toggleClass('d-none ')
        $('html, body').animate({
            scrollTop: $(".bla").offset().top   //id of div to be scrolled
            }, 3000);

        if (!form.hasClass('d-none')){
            $.ajax({
                url:`/comment/${post}/`,
                dataType:"json",
                success:function(data){
                    comments_tag.empty()
                    var comments = data.comments
                    comments.forEach(element=>{comments_tag.append(`<p class="text-left"><b>${element.user__display_name}</b>: ${element.body} </p><hr>`)})
                }
            })
        }
    })
     var is_authenticated = $("#is_authenticated").val()
     if (!is_authenticated){
         $("#button").on('click', function(event){
            event.preventDefault();
            $('#login-form').attr('action', `/login/?next=${window.location.pathname}#form`)
            $('#register').attr('href', `/register/?next=${window.location.pathname}#form`)

            $('#popup').click()
         })
     }
})