$(function(){

    //Detect the text from uploaded image
  $("#image_to_text").on("click", function(){
    var input = document.getElementById('imgInp');
    var image_link = $('#upload_image').attr('src');
    converted_data = image_link.split(",");
    data = converted_data[1];
    const byteCharacters = atob(data);

    var ittRequest = {'url':image_link}

    var xhr = new XMLHttpRequest();
    xhr.open("POST","/image-to-text",true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.responseType = "json";
    xhr.send(JSON.stringify(ittRequest));
    xhr.onload = function(evt){
      if (xhr.status === 200){
        console.log(xhr.response);
        document.getElementById("image-result").value="";
        
        for (var i=0; i<xhr.response["readResults"][0].lines.length; i++){
          document.getElementById("image-result").value += xhr.response["readResults"][0].lines[i].text+"\n";
        }
      }  
    }
    });

});