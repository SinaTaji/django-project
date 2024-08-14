function filter_products() {
    const filterPrice = $('#sl2').val();
    const startPrice = filterPrice.split(',')[0];
    const endPrice = filterPrice.split(',')[1];
    $('#start_price').val(startPrice);
    $('#end_price').val(endPrice);
    $('#filter_price').submit();

}

function page_number(PageNumber) {
    $('#page').val(PageNumber);
    $('#filter_price').submit();

}


function sendArticleComment() {
    var comment = $('#commentText').val();
    var articleId = $('#article_id').val();
    var parentId = $('#parent_id').val();

    $.ajax({
        url: '/article/add-article-comment/',
        type: 'POST',
        data: {
            text: comment,
            article: articleId,
            parent: parentId,
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
        },
        success: function (response) {
            if (response.status === 'success') {
                alert(response.message);
                location.reload();
            } else {
                console.log(response.errors);
                alert(response.message);
            }
        },
        error: function (xhr, status, error) {
            console.error(error);
            alert('خطایی رخ داده است.');
        }
    });
}

function fillParentId(parentId) {
    $('#parent_id').val(parentId);
    document.getElementById('comment_form').scrollIntoView({behavior: "smooth"});
}

function sendProductComment() {
    var comment = $('#commentText').val();
    var productId = $('#product_id').val();
    var parentId = $('#parent_id').val();

    $.ajax({
        url: '/product/add-products-comment/',
        type: 'POST',
        data: {
            text: comment,
            product: productId,
            parent: parentId,
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
        },
        success: function (response) {
            if (response.status === 'success') {
                alert(response.message);
                location.reload();
            } else {
                console.log(response.errors);
                alert(response.message);
            }
        },
        error: function (xhr, status, error) {
            console.error(error);
            alert('خطایی رخ داده است.');
        }
    });
}

function filleParentId(parentId) {
    $('#parent_id').val(parentId);
    document.getElementById('product_form').scrollIntoView({behavior: "smooth"});
}

function ShowLargeImage(ImgSrc) {
    $("#main-image").attr('src', ImgSrc);
    $("#show_image_large").attr('href', ImgSrc);
}


function GetProductId(ProductId) {
    const product_count = $("#product-count").val();
    const colorInput = document.querySelector('input[name="product-color"]:checked');
    let color_id = colorInput ? colorInput.value : null;
    const sideInput = document.querySelector('input[name="product-side"]:checked');
    let side = sideInput ? sideInput.value : null;

    if (document.querySelector('.color-options-new') && !color_id) {
        Swal.fire({
            title: 'اعلان',
            text: 'لطفا رنگ محصول را انتخاب کنید!',
            icon: 'error',
            showCancelButton: false,
            confirmButtonColor: '#3085d6',
            confirmButtonText: 'ممنون'
        });
        return;
    }


    if (document.querySelector('.side-selection') && !side) {
        Swal.fire({
            title: 'اعلان',
            text: 'لطفا سمت مورد نظر خود را انتخاب کنید!',
            icon: 'error',
            showCancelButton: false,
            confirmButtonColor: '#3085d6',
            confirmButtonText: 'ممنون'
        });
        return;
    }

    $.get('/order/add-order?products_id=' + ProductId + '&count=' + product_count + '&color_id=' + (color_id === 'default' ? '' : color_id) + '&side=' + (side || '')).then(res => {
        Swal.fire({
            title: 'اعلان',
            text: res.text,
            icon: res.icon,
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            confirmButtonText: res.confirmButtonText,
            cancelButtonText: res.cancelButtonText
        }).then((result) => {
            if (result.isConfirmed && res.status === 'not_auth') {
                window.location.href = '/user/login';
            }
            if (result.isConfirmed && res.status === 'success-add') {
                window.location.href = '/user-panel/user-basket';
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', function () {
    var mySwiper = new Swiper('.swiper-container', {
        slidesPerView: 'auto',
        speed: 800,
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
    });
});

const showSweetAlertMessage = (icon, title) => {
    if (typeof Swal !== 'undefined') {
        Swal.fire({
            icon: icon,
            title: title
        });
    } else {
        console.error('SweetAlert2 is not loaded');
    }
};

function removeOrderDetail(detailId) {
    $.get("/user-panel/remove-order-detail?detail_id=" + detailId).then(res => {
        if (res.status === 'success') {
            $("#order_detail_content").html(res.data);
        }
    })
}

function changeOrderDetail(detailId, state) {
    $.get("/user-panel/change-order-detail?detail_id=" + detailId + '&state=' + state).then(res => {
        if (res.status === 'success') {
            $("#order_detail_content").html(res.data);
        }
    })
}

document.addEventListener('DOMContentLoaded', (event) => {
    const colorOptions = document.querySelectorAll('input[name="product-color"]');
    const priceElement = document.getElementById('price_value');

    colorOptions.forEach(option => {
        option.addEventListener('change', function () {
            const selectedPrice = parseFloat(this.getAttribute('data-price'));
            if (!isNaN(selectedPrice)) {
                priceElement.textContent = selectedPrice.toLocaleString('fa-IR');
            } else {
                console.error('قیمت عدد نیست: ', this.getAttribute('data-price'));
            }
        });
    });
});


function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function (event) {
    if (!event.target.matches('.dropbtn') && !event.target.closest('.dropdown-content')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const sortButtonDesc = document.getElementById('sort-price-desc');
    const productList = document.getElementById('product-list');
    const products = Array.from(document.getElementsByClassName('product'));

    sortButtonDesc.addEventListener('click', function () {
        const sortedProducts = products.sort((a, b) => {
            const priceA = parseFloat(a.getAttribute('data-price'));
            const priceB = parseFloat(b.getAttribute('data-price'));
            return priceB - priceA;
        });

        productList.innerHTML = '';

        sortedProducts.forEach(product => {
            productList.appendChild(product);
        });
    });
});

function toggleDropup(dropupId) {
    var dropup = document.getElementById(dropupId);
    dropup.classList.toggle("show");
}

// Close the dropup if the user clicks outside of it
window.onclick = function (event) {
    if (!event.target.matches('.dropbtnn')) {
        var dropups = document.getElementsByClassName("dropup-content");
        for (var i = 0; i < dropups.length; i++) {
            var openDropup = dropups[i];
            if (openDropup.classList.contains('show')) {
                openDropup.classList.remove('show');
            }
        }
    }
}


function sortProductsByPrice() {
    const productList = document.getElementById('product-list');
    const products = Array.from(productList.getElementsByClassName('product-item'));

    products.sort((a, b) => {
        return parseInt(a.getAttribute('data-price')) - parseInt(b.getAttribute('data-price'));
    });

    products.forEach(product => {
        productList.appendChild(product);
    });
}

function sortProductsByPriceg() {
    const productList = document.getElementById('product-list');
    const products = Array.from(productList.getElementsByClassName('product-item'));

    products.sort((a, b) => {
        return parseInt(b.getAttribute('data-price')) - parseInt(a.getAttribute('data-price'));
    });

    products.forEach(product => {
        productList.appendChild(product);
    });
}

function sortProductsById() {
    const productList = document.getElementById('product-list');
    const products = Array.from(productList.getElementsByClassName('product-item'));

    products.sort((a, b) => {
        return parseInt(b.getAttribute('data-id')) - parseInt(a.getAttribute('data-id'));
    });

    products.forEach(product => {
        productList.appendChild(product);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const colorBoxes = document.querySelectorAll('.color-box');
    colorBoxes.forEach(box => {
        box.style.backgroundColor = box.getAttribute('data-color');
    });
});

document.getElementById('pay-w-z').addEventListener('click', function (event) {
    event.preventDefault();

    var form = document.getElementById('payment-form');
    var submitButton = document.getElementById('submit-btn');
    var errors = false;


    document.querySelectorAll('.error').forEach(function (element) {
        element.classList.remove('error');
    });

    form.querySelectorAll('input, select, textarea').forEach(function (field) {
        if (!field.value) {
            field.classList.add('error');
            errors = true;
        }
    });

    if (errors) {
        window.scrollTo(
            {
                top: 20,
                behavior: "smooth",
            }
        )
    } else {
        submitButton.click();
    }
});

