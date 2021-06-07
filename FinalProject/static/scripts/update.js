$(function(){

    $("#update_b").on("click", function() {
        var soup_div = document.getElementById("soup");
        var topping_div = document.getElementById("topping");
        var level_div = document.getElementById("level");
        var dish_div = document.getElementById("dish");

        var lang = $("#lang").val();
        var m_id = $("#r_id").val();

        soup_data_list = [];
        topping_data_list = [];
        level_data_list = [];
        dish_data_list = [];
        
        $(soup_div).find(".w3-card").each(function(){
            soupName=$(this).find("#name").val() || "";
            soupPrice=$(this).find('#price').val() || "";
            soup_data = {"name":soupName,"price":soupPrice}
            soup_data_list.push(soup_data);
        })
        $(topping_div).find(".w3-card").each(function(){
            topName=$(this).find("#nameT").val()||"";
            topPrice=$(this).find('#price').val()||"";
            topping_data = {"name":topName,"price":topPrice}
            topping_data_list.push(topping_data);
        })
        $(level_div).find(".myinput").each(function(){
            taste=$(this).val()||"";
            level_data_list.push(taste);
        })
        $(dish_div).find(".w3-card").each(function(){
            dishName=$(this).find("#name").val();
            dishPrice=$(this).find('#price').val();
            dishDescription = $(this).find('#description').val()||"";
            dish_data = {"name":dishName,"price":dishPrice,"description":dishDescription}
            dish_data_list.push(dish_data);
        })
        
        console.log(soup_data_list,topping_data_list,level_data_list,dish_data_list);
        data_input = {"lang":lang,"m_id":m_id, "dish":dish_data_list,
                        "topping":topping_data_list,"soup":soup_data_list,"level":level_data_list}
        $.ajax({
            url: '/manage/update',
            method: 'POST',
            headers: {
                'Content-Type':'application/json'
            },
            dataType: 'json',
            data: JSON.stringify(data_input),
            success: function(data) {
                console.log("done");
                if(!alert('Update Success!')){window.location.reload();}
            }
        });
    })
});