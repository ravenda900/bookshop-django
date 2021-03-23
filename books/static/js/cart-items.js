(function ($) {
    $('.book-quantity-input').keyup(function () {
        const $row = $(this).parents('tr');

        const price = parseFloat($row.find('.book-price').text());
        const quantity = parseInt($(this).val()) || 1;

        $row.find('.book-total').text(price * quantity);
    });
}(jQuery));