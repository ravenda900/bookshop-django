(function ($) {
    $('.book-quantity-input').keyup(function () {
        const $row = $(this).parents('tr');
        const $table = $(this).parents('table');

        const price = parseFloat($row.find('.book-price').text());
        const quantity = parseInt($(this).val()) || 1;
        const bookPrice = price * quantity;
        let totalPrice = 0;

        $row.find('.book-total').text(bookPrice);

        $table.find('tbody > tr').each((index, elem) => {
            const $parentRow = $(elem);
            const bookPartialPrice = parseFloat($parentRow.find('.book-total').text());

            totalPrice += (bookPartialPrice || parseFloat($parentRow.find('.book-price').text()));
        });
        $('#totalPrice').text(`₱ ${totalPrice}`);
    });
}(jQuery));