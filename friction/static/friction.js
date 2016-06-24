var settingsElement = document.getElementById('settings');
var settingsToggle = document.getElementById('settings-toggle');
var filterElement = document.getElementById('filter');
var submitElement = document.getElementById('submit');

function handleItems() {
  var resp = JSON.parse(this.responseText);
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
  settingsElement.classList.toggle('shown');
}

function showSettings() {
  if (!settingsElement.classList.contains('shown')) toggleSettings();
  filterElement.focus();
}

window.addEventListener('keyup', function(e) {
  if (e.keyCode == 79) showSettings();
});

settingsToggle.addEventListener('click', function(e) {
  toggleSettings();
  e.preventDefault();
});

getItems();
