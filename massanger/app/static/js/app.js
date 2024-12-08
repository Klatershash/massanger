function sendMessage(chat_id, login){
    let messageInput = $('#messageInput').val();
    let csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
    let image = document.getElementById('file').files[0];


    let data = {
        message: messageInput,
        chat: chat_id,
        csrfmiddlewaretoken: csrfmiddlewaretoken
    };

     if(image){
        let d = {};
        let reader = new FileReader();
        reader.onload = function(e){
              d['file'] = e.target.result;
              d['filename'] = image.name;
              data['json_file'] = d;

        };
        reader.readAsDataURL(file);
         console.log(JSON.stringify(data));
      
        //data['image'] = image;
        //data['imagename'] = image.name;
        
    }else{
        data['image'] = '';
       data['imagename'] = '';
    }
    console.log(data);

    $.ajax({
        url: '/ajaxAddMessage',
        method: 'POST',
        dataType: 'html',
        data:data,
        success: function(response){
            if(response == 'Ok'){
                let datetime = new Date();
                let m = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь'];
                datetime.toLocaleString('ru-RU');
                let res_date = `${datetime.getDate()} ${m[datetime.getMonth()]} ${datetime.getFullYear()} г. ${datetime.getHours()}:${datetime.getMinutes()}`;
                let content = '<div class="message " style="text-align: right"><span class="user">'+login+'</span><span class="text">'+messageInput+'</span><span class="datetime">'+res_date+'</span></div>';

                $('#chatContainer').append(content);
                $('#messageInput').val('');
            }
        }
    });
}