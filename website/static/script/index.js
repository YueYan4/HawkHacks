{
    const search = document.querySelector('.btn');

    let maker;
    let model;
    let year;

    search.addEventListener('click', () => {
        maker = document.querySelector('.name-input').value;
        model = document.querySelector('.model-input').value;
        year = document.querySelector('.year-input').value;
        console.log(maker, model, year);

        const car_value = JSON.stringify({ maker, model, year });
        console.log(car_value);

        window.alert(car_value);
        $.ajax({
            url: '/search',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(car_value),
        });
    });
}
