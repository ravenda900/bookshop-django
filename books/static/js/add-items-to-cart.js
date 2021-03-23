(function ($) {
    $('.btn-add-cart').click(function (e) {
        let bookId = $(this).data('book-id');

        $.ajax({
            method: 'post',
            dataType: 'json',
            url: '/add-items-to-cart/' + bookId,
            success: (response) => {
                if (response.success) {
                    const $cartItemsCount = $('#cart-items-count');
                    let cartItemsCount = parseInt($cartItemsCount.text());

                    $cartItemsCount.text(++cartItemsCount);

                    alert(response.success);
                }
            },
            error: (xhr, status, error) => {
                alert(xhr.responseJSON.error);
            }
        });
    });
}(jQuery));