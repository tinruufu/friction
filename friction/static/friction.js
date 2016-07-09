var settingsToggle = document.getElementById('settings-toggle');
var filterElement = document.getElementById('filter');
var idElement = document.getElementById('id');
var rtl = document.getElementById('rtl').checked;
var submitElement = document.getElementById('submit');
var messengerElement = document.getElementById('messenger');

function handleItems() {
  messengerElement.innerHTML = '';

  if (this.status >= 500) {
    document.title = 'aww jeez';
    messengerElement.innerHTML = "sorry, something bad happened<br/><br/>the server has probably printed or logged more information<br/><br/>it'd be very nice if you could <a href='https://github.com/tinruufu/friction/issues'>file a bug</a> about this";
  }

  var resp = JSON.parse(this.responseText);

  if (this.status != 200) {
    messengerElement.innerHTML = resp.message;
    document.title = 'sorry :<';
    showSettings();
    return;
  }

  if (!idElement.value) {
    window.history.replaceState({}, resp.title, window.location.pathname + '?id=' + resp.id + '&' + window.location.search.replace(/^\?/, ''));
  }

  var index = 0;

  if (rtl) {
    resp.photoswipe.reverse();
    index = resp.photoswipe.length - 1;
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
        barsSize: {top: 0, bottom: 0},
        index: index
      }
  );

  gallery.listen('close', function() {submitForm();});
  window.addEventListener('keypress', function(e) {
    if (e.keyCode == 13) submitForm();
  });
  gallery.init();
}

// *some* browsers won't let us submit the form unless we change something, so,,
function changeForm() {
  filterElement.value += ' ';
}

function submitForm() {
  changeForm();
  submitElement.click();
}

function getItems() {
  var url;

  if (idElement.value) url = '/items?id=' + encodeURIComponent(idElement.value);
  else url = '/items?f=' + encodeURIComponent(filterElement.value);

  var itemsRequest = new XMLHttpRequest();
  document.title = 'loading';
  itemsRequest.addEventListener('load', handleItems);
  itemsRequest.open('GET', url);
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
