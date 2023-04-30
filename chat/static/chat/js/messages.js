let input_message = $('#input-message')
let message_body = $('.msg_card_body')
let send_message_form = $('#send-message-form')
const USER_ID = $('#logged-in-user').val()

let loc = window.location
let wsStart = 'ws://'

if(loc.protocol === 'https:') {
    wsStart = 'wss://'
}
let endpoint = wsStart + loc.host + loc.pathname

var socket = new WebSocket(endpoint)

socket.onopen = async function(e){
    console.log('open', e)
    send_message_form.on('submit', function (e){
        e.preventDefault()
        let message = input_message.val()
        let send_to = get_active_other_user_id()
        let thread_id = get_active_thread_id()

        let data = {
            'message': message,
            'sent_by': USER_ID,
            'send_to': send_to,
            'thread_id': thread_id
        }
        data = JSON.stringify(data)
        socket.send(data)
        $(this)[0].reset()

        
    })
    let message_body = $('.messages-wrapper.is_active .msg_card_body');
        message_body.animate({
            scrollTop: message_body.get(0).scrollHeight
        }, 100);
}

socket.onmessage = async function(e){
    console.log('message', e)
    let data = JSON.parse(e.data)
    let message = data['message']
    let sent_by_id = data['sent_by']
    let thread_id = data['thread_id']
    newMessage(message, sent_by_id, thread_id)
}

socket.onerror = async function(e){
    console.log('error', e)
}

socket.onclose = async function(e){
    console.log('close', e)
}

socket.timeout = 9999999; 



function newMessage(message, sent_by_id, thread_id) {
	if ($.trim(message) === '') {
		return false;
	}
	let message_element;
	let chat_id = 'chat_' + thread_id
	if(sent_by_id == USER_ID){
	    message_element = `
			<div class="d-flex mb-4 replied">
				<div class="msg_cotainer_send">
					${message}
					<span class="msg_time_send"></span>
				</div>
				
			</div>
	    `
    }
	else{
	    let now = new Date();
	    let time = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
	    message_element = `
           <div class="d-flex mb-4 received">
             
              <div class="msg_cotainer">
                 ${message}
              <span class="msg_time">${time}</span>
              </div>
           </div>
        `
    }

    let message_body = $('.messages-wrapper[chat-id="' + chat_id + '"] .msg_card_body')
    message_body.append($(message_element))
    
    // Insert current time into span element with class "msg_time_send"
    let now = new Date();
    let time = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    message_body.find('.msg_time_send:last, .msg_time:last').text(time)
    
    message_body.animate({
        scrollTop: message_body.get(0).scrollHeight
    }, 100);
	input_message.val(null);
}

$('.contact-li').on('click', function () {
    // remove "active" class from previously selected contact
    $('.contacts .active').removeClass('active')
  
    // add "active" class to the clicked contact
    $(this).addClass('active')
  
    // message wrappers
    let chat_id = $(this).attr('chat-id')
    $('.messages-wrapper.is_active').removeClass('is_active')
    $('.messages-wrapper[chat-id="' + chat_id + '"]').addClass('is_active')
  
    // scroll to latest conversation
    let message_body = $('.messages-wrapper.is_active .msg_card_body');
    message_body.animate({
      scrollTop: message_body.get(0).scrollHeight
    }, 100);
  })
  

function get_active_other_user_id(){
    let other_user_id = $('.messages-wrapper.is_active').attr('other-user-id')
    other_user_id = $.trim(other_user_id)
    return other_user_id
}

function get_active_thread_id(){
    let chat_id = $('.messages-wrapper.is_active').attr('chat-id')
    let thread_id = chat_id.replace('chat_', '')
    return thread_id
}

$(document).ready(function() {
    // Add event listener to the "Message Seller" button
    $("form").submit(function(event) {
        // Prevent the form from submitting synchronously
        event.preventDefault();
        
        // Get the form data
        var formData = {
            'author_id' : $('input[name=author_id]').val()
        };
        
        // Send an Ajax request to the server
        $.ajax({
            type: 'POST',
            url: '{% url "messages" %}',
            data: formData,
            dataType: 'json',
            encode: true
        })
        
        // Success function, handle server response
        .done(function(data) {
            console.log(data);
            // Update the DOM or perform other actions
        })
        
        // Failure function, handle errors
        .fail(function(data) {
            console.log(data);
            // Handle errors
        });
    });
});
