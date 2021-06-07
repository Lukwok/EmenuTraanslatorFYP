$(function(){
    $('.checkbox-group1').change(function() {
        var oprice = document.getElementById("oprice").value;
        var meunid = document.getElementById("mid").value;
        var soup = $('input[name="soup"]:checked').val() | 0;
        $('.checkbox-group1').each(function() {
            var values = [];
            $(this).find('input[type="checkbox"]:checked').each(function(i, v) {
            values.push($(v).val());
            });
            var add_list = {'food_array': values, 'oprice':oprice, 'mid':meunid, 'soup':soup}
            
                $.ajax({
                    url: '/add_sum',
                    method: 'POST',
                    headers: {
                        'Content-Type':'application/json'
                    },
                    dataType: 'json',
                    data: JSON.stringify(add_list),
                    success: function(data) {
                        console.log(data)
                        document.getElementById("totalsum").innerHTML= '$' + data.toFixed(1);
                        $("#price").val(data.toFixed(1));
                    }
                });
                console.log(values,soup)
        })
    });

    $(document).on('click', '[name="soup"]', function () {
        var oprice = document.getElementById("oprice").value;
        var meunid = document.getElementById("mid").value;
        var soup = $('input[name="soup"]:checked').val() | 0;
        var values = [];
        $('.checkbox-group1').each(function() {
            $(this).find('input[type="checkbox"]:checked').each(function(i, v) {
            values.push($(v).val());
            });
        })
            var add_list = {'food_array': values, 'oprice':oprice, 'mid':meunid, 'soup':soup}
            
                $.ajax({
                    url: '/add_sum',
                    method: 'POST',
                    headers: {
                        'Content-Type':'application/json'
                    },
                    dataType: 'json',
                    data: JSON.stringify(add_list),
                    success: function(data) {
                        console.log(data)
                        document.getElementById("totalsum").innerHTML= '$' + data.toFixed(1);
                        $("#price").val(data.toFixed(1));
                    }
                });
                console.log(values,soup)
    });


});