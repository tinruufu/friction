var settingsToggle = document.getElementById('settings-toggle');
var filterElement = document.getElementById('filter');
var submitElement = document.getElementById('submit');
var messengerElement = document.getElementById('messenger');

function handleItems() {
  var resp = JSON.parse(this.responseText);

  if (this.status != 200) {
    messengerElement.innerHTML = resp.message;
    document.title = 'sorry :<';
    showSettings();
    return;
  }

  document.title = resp.title;
  var gallery = new PhotoSwipe(
      document.getElementById('pswp'),
      PhotoSwipeUI_Default, 
      resp.photoswipe,
      {
        spacing: 0,
        history: false,
        escKey: true,
        barsSize: {top: 0, bottom: 0}
      }
  );
  gallery.listen('close', function() {submitElement.click();});
  window.addEventListener('keypress', function(e) {
    if (e.keyCode == 13) submitElement.click();
  });
  gallery.init();
}

function getItems() {
  var itemsRequest = new XMLHttpRequest();
  document.title = 'loading';
  itemsRequest.addEventListener('load', handleItems);
  itemsRequest.open('GET', '/items?f=' + encodeURIComponent(filterElement.value));
  itemsRequest.send();
}


function toggleSettings() {
  document.body.classList.toggle('settings-shown');
}

function showSettings() {
  if (!document.body.classList.contains('settings-shown')) toggleSettings();
  filterElement.focus();
}

window.addEventListener('keyup', function(e) {
  if (e.keyCode == 79) showSettings();
});

settingsToggle.addEventListener('click', function(e) {
  toggleSettings();
  e.preventDefault();
});

setTimeout(function() {
  settingsToggle.classList.remove('just-loaded');
}, 1000);

getItems();
