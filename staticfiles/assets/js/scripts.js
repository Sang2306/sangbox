(function (window, undefined) {
    'use strict';

    /*
    NOTE:
    ------
    PLACE HERE YOUR OWN JAVASCRIPT CODE IF NEEDED
    WE WILL RELEASE FUTURE UPDATES SO IN ORDER TO NOT OVERWRITE YOUR JAVASCRIPT CODE PLEASE CONSIDER WRITING YOUR SCRIPT HERE.  */
    let $new_pass_input = $('#inputPassword3');
    let $confirm_pass_input = $('#inputPassword4');

    $confirm_pass_input.keyup((e) => {
        if ($confirm_pass_input.val() !== $new_pass_input.val()) {
            $('#msg').text('Mật khẩu không khớp!');
            $('#okbtn').attr('disabled', 'disabled');
        } else {
            $('#msg').text('');
            $('#okbtn').removeAttr('disabled');
        }
    });

    //function to handle ajax article


})(window);