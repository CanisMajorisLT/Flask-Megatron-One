__author__ = 'vyt'
from bs4 import BeautifulSoup
import re

page = """<div id="main" class="grid-c">
<div id="content" class="inbox-v2 ads-v2">
<div id="inbox-tabview" class="inbox-tabview">
<div class="content">
<div id="message-list" class="" data-count="1115" page-size="10" data-unread-msg="0" data-pending-inv="0">
<form action="/inbox/bulk_action" method="POST" name="bulkActionForm" novalidate="novalidate">
<div class="topActionBar">
<div class="topActions-new alldropdown-new split-dropdown">
<span class="more-options dropdown-hover clickclose">
<span class='clear-button dropdown-trigger'>
All<span class="caret"></span>
</span>
<dl class="more-options-menu new-options-actions">
<dd><a href="/inbox/#sent?subFilter=none&amp;keywords=&amp;sortBy=">All</a></dd>
<dd><a href="/inbox/#sent?subFilter=message&amp;keywords=&amp;sortBy=">Messages</a></dd>
<dd><a href="/inbox/#sent?subFilter=invitation&amp;keywords=&amp;sortBy=">Invitations</a></dd>
<dd><a href="/inbox/#sent?subFilter=userStarred&amp;keywords=&amp;sortBy=">Starred</a></dd>
<dd><a href="/inbox/#sent?subFilter=inmail&amp;keywords=&amp;sortBy=">InMail</a></dd>
</dl>
</span>
</div>
<ul class="topActions-new bulkContainer-new standard-actions inbox-actions-new">
<li bulk-action="bulkArchive">
<a class="clear-button" href="#">
<span class="action-icon archive"></span>
Archive
</a>
</li>
<li bulk-action="bulkTrash">
<a class="clear-button" href="#">
<span class="action-icon trash"></span>
Trash
</a>
</li>
<li class='bulkcheck'>
<label for="checkbox-bulkcheck" class="hidden-accessible">Select all messages.</label>
<input class="bulk-chk" type="checkbox" id="checkbox-bulkcheck">
</li>
</ul>
</div>
<ol class="inbox-list ">
<li data-gid="S5935107970185596928_500" class="inbox-item message-item subs-inbox-fac">
<img alt="Vytenis Butkevičius" class="photo" height="60" src="https://media.licdn.com/mpr/mpr/shrink_60_60/p/1/000/007/144/2775907.jpg" width="60"/>
<div class="item-content actions-left">
<label for="checkbox_S5935107970185596928_500" class='hidden-accessible'>Vytenis Butkevičius</label>
<input class="chk" type="checkbox" name="mboxItemGIDs" value="S5935107970185596928_500" id="checkbox_S5935107970185596928_500">
<div class="date">
<span class="time-millis hidden">Mon Nov 03 18:40:09 UTC 2014</span>
<span class="today hidden">Today</span>
<span class="yesterday hidden">Yesterday</span>
<span class="this-year hidden">Nov 3</span>
<span class="past hidden">Nov 3, 2014</span>
</div>
<span class="participants">
<span class="to">To: </span>
Antanas Končius
</span>
<div class="folder-subject">
<p class="subject">
<a class="detail-link " href="/inbox/#detail?itemId=S5935107970185596928_500&amp;trk=COMM_NI">
RE: Potencialiai įdomi pozicija
</a>
</p>
</div>
<p class="preview  not-empty">Sveiki, Antanai,
Ačiū už atsakymą. :)
Pagarbiai
Vytenis
On 11/03/14 10:32 AM, Antanas Končius wrote:
--------------------
...</p>
<span title="Star">
<a data-action="star" data-action-url="/inbox/action?mboxItemGID=S5935107970185596928_500&amp;actionType=star&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="flag-link" href="/inbox/action?mboxItemGID=S5935107970185596928_500&amp;actionType=star&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Star</a>
</span>
<span title="Unstar">
<a data-action="unstar" data-action-url="/inbox/action?mboxItemGID=S5935107970185596928_500&amp;actionType=unstar&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="unflag-link" href="/inbox/action?mboxItemGID=S5935107970185596928_500&amp;actionType=unstar&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Unstar</a>
</span>
<ul class="inbox-actions">
<li class="replyToSender">
<a href="/inbox/#msgToConns?itemID=S5935107970185596928_500&amp;displayReplyAll=" data-action-url="" data-action="replyAllMEBC">Reply</a>
</li>
<li class="forward">
<a data-action="forward" data-action-url="" class="" href="/inbox/#action?mboxItemGID=S5935107970185596928_500&amp;actionType=forward&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Forward</a>
</li>
<li class="archive">
<a data-action="archive" data-action-url="/inbox/action?mboxItemGID=S5935107970185596928_500&amp;actionType=archive&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="" href="/inbox/action?mboxItemGID=S5935107970185596928_500&amp;actionType=archive&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Archive</a>
</li>
<li class="trash">
<a data-action="trash" data-action-url="/inbox/action?mboxItemGID=S5935107970185596928_500&amp;actionType=trash&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="" href="/inbox/action?mboxItemGID=S5935107970185596928_500&amp;actionType=trash&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Delete</a>
</li>
</ul>
</div>
</li>
<li data-gid="S5935027418162036736_500" class="inbox-item message-item subs-inbox-fac">
<img src="https://static.licdn.com/scds/common/u/img/themes/katy/ghosts/profiles/ghost_profile_40x40_v1.png" class="photo" alt="Vytenis Butkevičius" height="60" width="60">
<div class="item-content actions-left">
<label for="checkbox_S5935027418162036736_500" class='hidden-accessible'>Vytenis Butkevičius</label>
<input class="chk" type="checkbox" name="mboxItemGIDs" value="S5935027418162036736_500" id="checkbox_S5935027418162036736_500">
<div class="date">
<span class="time-millis hidden">Mon Nov 03 13:20:03 UTC 2014</span>
<span class="today hidden">Today</span>
<span class="yesterday hidden">Yesterday</span>
<span class="this-year hidden">Nov 3</span>
<span class="past hidden">Nov 3, 2014</span>
</div>
<span class="participants">
<span class="to">To: </span>
Aurelijus Janeliunas
</span>
<div class="folder-subject">
<p class="subject">
<a class="detail-link " href="/inbox/#detail?itemId=S5935027418162036736_500&amp;trk=COMM_NI">
Join my network on LinkedIn
</a>
</p>
</div>
<p class="preview  not-empty">Laba diena,
Esu personalo atrankų konsultantas ir norėčiau Jus prisijungti prie savo profesionalų tinklo LinkedIn. Net jei šiuo metu ir...</p>
<span title="Star">
<a data-action="star" data-action-url="/inbox/action?mboxItemGID=S5935027418162036736_500&amp;actionType=star&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="flag-link" href="/inbox/action?mboxItemGID=S5935027418162036736_500&amp;actionType=star&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Star</a>
</span>
<span title="Unstar">
<a data-action="unstar" data-action-url="/inbox/action?mboxItemGID=S5935027418162036736_500&amp;actionType=unstar&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="unflag-link" href="/inbox/action?mboxItemGID=S5935027418162036736_500&amp;actionType=unstar&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Unstar</a>
</span>
<ul class="inbox-actions">
<li class="replyToSender">
<a href="/inbox/#msgToConns?itemID=S5935027418162036736_500&amp;displayReplyAll=" data-action-url="" data-action="replyAllMEBC">Reply</a>
</li>
<li class="forward">
<a data-action="forward" data-action-url="" class="" href="/inbox/#msgToConns?itemID=S5935027418162036736_500&amp;displayForward=&amp;trk=COMM_NI">Forward</a>
</li>
<li class="archive">
<a data-action="archive" data-action-url="/inbox/action?mboxItemGID=S5935027418162036736_500&amp;actionType=archive&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="" href="/inbox/action?mboxItemGID=S5935027418162036736_500&amp;actionType=archive&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Archive</a>
</li>
<li class="trash">
<a data-action="trash" data-action-url="/inbox/action?mboxItemGID=S5935027418162036736_500&amp;actionType=trash&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="" href="/inbox/action?mboxItemGID=S5935027418162036736_500&amp;actionType=trash&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Delete</a>
</li>
</ul>
</div>
</li>
<li data-gid="S5935026669319397379_500" class="inbox-item message-item subs-inbox-fac">
<img alt="Vytenis Butkevičius" class="photo" height="60" src="https://media.licdn.com/mpr/mpr/shrink_60_60/p/3/000/087/1aa/221a5d3.jpg" width="60"/>
<div class="item-content actions-left">
<label for="checkbox_S5935026669319397379_500" class='hidden-accessible'>Vytenis Butkevičius</label>
<input class="chk" type="checkbox" name="mboxItemGIDs" value="S5935026669319397379_500" id="checkbox_S5935026669319397379_500">
<div class="date">
<span class="time-millis hidden">Mon Nov 03 13:17:05 UTC 2014</span>
<span class="today hidden">Today</span>
<span class="yesterday hidden">Yesterday</span>
<span class="this-year hidden">Nov 3</span>
<span class="past hidden">Nov 3, 2014</span>
</div>
<span class="participants">
<span class="to">To: </span>
Tadas Sugintas
</span>
<span class="item-status item-status-accepted">
(Accepted)
</span>
<div class="folder-subject">
<p class="subject">
<a class="detail-link " href="/inbox/#detail?itemId=S5935026669319397379_500&amp;trk=COMM_NI">
Join my network on LinkedIn
</a>
</p>
</div>
<p class="preview  not-empty">Laba diena,
Esu personalo atrankų konsultantas ir norėčiau Jus prisijungti prie savo profesionalų tinklo LinkedIn. Net jei šiuo metu ir...</p>
<span title="Star">
<a data-action="star" data-action-url="/inbox/action?mboxItemGID=S5935026669319397379_500&amp;actionType=star&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="flag-link" href="/inbox/action?mboxItemGID=S5935026669319397379_500&amp;actionType=star&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Star</a>
</span>
<span title="Unstar">
<a data-action="unstar" data-action-url="/inbox/action?mboxItemGID=S5935026669319397379_500&amp;actionType=unstar&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="unflag-link" href="/inbox/action?mboxItemGID=S5935026669319397379_500&amp;actionType=unstar&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Unstar</a>
</span>
<ul class="inbox-actions">
<li class="replyToSender">
<a href="/inbox/#msgToConns?itemID=S5935026669319397379_500&amp;displayReplyAll=" data-action-url="" data-action="replyAllMEBC">Reply</a>
</li>
<li class="forward">
<a data-action="forward" data-action-url="" class="" href="/inbox/#msgToConns?itemID=S5935026669319397379_500&amp;displayForward=&amp;trk=COMM_NI">Forward</a>
</li>
<li class="archive">
<a data-action="archive" data-action-url="/inbox/action?mboxItemGID=S5935026669319397379_500&amp;actionType=archive&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="" href="/inbox/action?mboxItemGID=S5935026669319397379_500&amp;actionType=archive&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Archive</a>
</li>
<li class="trash">
<a data-action="trash" data-action-url="/inbox/action?mboxItemGID=S5935026669319397379_500&amp;actionType=trash&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="" href="/inbox/action?mboxItemGID=S5935026669319397379_500&amp;actionType=trash&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Delete</a>
</li>
</ul>
</div>
</li>
<li data-gid="S5935026101108641792_500" class="inbox-item message-item subs-inbox-fac">
<img alt="Vytenis Butkevičius" class="photo" height="60" src="https://media.licdn.com/mpr/mpr/shrink_60_60/p/4/005/056/2a3/30da150.jpg" width="60"/>
<div class="item-content actions-left">
<label for="checkbox_S5935026101108641792_500" class='hidden-accessible'>Vytenis Butkevičius</label>
<input class="chk" type="checkbox" name="mboxItemGIDs" value="S5935026101108641792_500" id="checkbox_S5935026101108641792_500">
<div class="date">
<span class="time-millis hidden">Mon Nov 03 13:14:49 UTC 2014</span>
<span class="today hidden">Today</span>
<span class="yesterday hidden">Yesterday</span>
<span class="this-year hidden">Nov 3</span>
<span class="past hidden">Nov 3, 2014</span>
</div>
<span class="participants">
<span class="to">To: </span>
Pranas Kieras
</span>
<span class="item-status item-status-accepted">
(Accepted)
</span>
<div class="folder-subject">
<p class="subject">
<a class="detail-link " href="/inbox/#detail?itemId=S5935026101108641792_500&amp;trk=COMM_NI">
Join my network on LinkedIn
</a>
</p>
</div>
<p class="preview  not-empty">I&#39;d like to add you to my professional network on LinkedIn.
- Vytenis Butkevičius</p>
<span title="Star">
<a data-action="star" data-action-url="/inbox/action?mboxItemGID=S5935026101108641792_500&amp;actionType=star&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="flag-link" href="/inbox/action?mboxItemGID=S5935026101108641792_500&amp;actionType=star&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Star</a>
</span>
<span title="Unstar">
<a data-action="unstar" data-action-url="/inbox/action?mboxItemGID=S5935026101108641792_500&amp;actionType=unstar&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="unflag-link" href="/inbox/action?mboxItemGID=S5935026101108641792_500&amp;actionType=unstar&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Unstar</a>
</span>
<ul class="inbox-actions">
<li class="replyToSender">
<a href="/inbox/#msgToConns?itemID=S5935026101108641792_500&amp;displayReplyAll=" data-action-url="" data-action="replyAllMEBC">Reply</a>
</li>
<li class="forward">
<a data-action="forward" data-action-url="" class="" href="/inbox/#msgToConns?itemID=S5935026101108641792_500&amp;displayForward=&amp;trk=COMM_NI">Forward</a>
</li>
<li class="archive">
<a data-action="archive" data-action-url="/inbox/action?mboxItemGID=S5935026101108641792_500&amp;actionType=archive&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="" href="/inbox/action?mboxItemGID=S5935026101108641792_500&amp;actionType=archive&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Archive</a>
</li>
<li class="trash">
<a data-action="trash" data-action-url="/inbox/action?mboxItemGID=S5935026101108641792_500&amp;actionType=trash&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="" href="/inbox/action?mboxItemGID=S5935026101108641792_500&amp;actionType=trash&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Delete</a>
</li>
</ul>
</div>
</li>
<li data-gid="S5935025757054083072_500" class="inbox-item message-item subs-inbox-fac">
<img src="https://static.licdn.com/scds/common/u/img/themes/katy/ghosts/profiles/ghost_profile_40x40_v1.png" class="photo" alt="Vytenis Butkevičius" height="60" width="60">
<div class="item-content actions-left">
<label for="checkbox_S5935025757054083072_500" class='hidden-accessible'>Vytenis Butkevičius</label>
<input class="chk" type="checkbox" name="mboxItemGIDs" value="S5935025757054083072_500" id="checkbox_S5935025757054083072_500">
<div class="date">
<span class="time-millis hidden">Mon Nov 03 13:13:27 UTC 2014</span>
<span class="today hidden">Today</span>
<span class="yesterday hidden">Yesterday</span>
<span class="this-year hidden">Nov 3</span>
<span class="past hidden">Nov 3, 2014</span>
</div>
<span class="participants">
<span class="to">To: </span>
Aurimas Liska
</span>
<div class="folder-subject">
<p class="subject">
<a class="detail-link " href="/inbox/#detail?itemId=S5935025757054083072_500&amp;trk=COMM_NI">
Join my network on LinkedIn
</a>
</p>
</div>
<p class="preview  not-empty">I&#39;d like to add you to my professional network on LinkedIn.
- Vytenis Butkevičius</p>
<span title="Star">
<a data-action="star" data-action-url="/inbox/action?mboxItemGID=S5935025757054083072_500&amp;actionType=star&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="flag-link" href="/inbox/action?mboxItemGID=S5935025757054083072_500&amp;actionType=star&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Star</a>
</span>
<span title="Unstar">
<a data-action="unstar" data-action-url="/inbox/action?mboxItemGID=S5935025757054083072_500&amp;actionType=unstar&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="unflag-link" href="/inbox/action?mboxItemGID=S5935025757054083072_500&amp;actionType=unstar&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Unstar</a>
</span>
<ul class="inbox-actions">
<li class="replyToSender">
<a href="/inbox/#msgToConns?itemID=S5935025757054083072_500&amp;displayReplyAll=" data-action-url="" data-action="replyAllMEBC">Reply</a>
</li>
<li class="forward">
<a data-action="forward" data-action-url="" class="" href="/inbox/#msgToConns?itemID=S5935025757054083072_500&amp;displayForward=&amp;trk=COMM_NI">Forward</a>
</li>
<li class="archive">
<a data-action="archive" data-action-url="/inbox/action?mboxItemGID=S5935025757054083072_500&amp;actionType=archive&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="" href="/inbox/action?mboxItemGID=S5935025757054083072_500&amp;actionType=archive&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Archive</a>
</li>
<li class="trash">
<a data-action="trash" data-action-url="/inbox/action?mboxItemGID=S5935025757054083072_500&amp;actionType=trash&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="" href="/inbox/action?mboxItemGID=S5935025757054083072_500&amp;actionType=trash&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Delete</a>
</li>
</ul>
</div>
</li>
<li data-gid="S5935025294661423104_500" class="inbox-item message-item subs-inbox-fac">
<img alt="Vytenis Butkevičius" class="photo" height="60" src="https://media.licdn.com/mpr/mpr/shrink_60_60/p/1/005/07c/2ce/17c4eab.jpg" width="60"/>
<div class="item-content actions-left">
<label for="checkbox_S5935025294661423104_500" class='hidden-accessible'>Vytenis Butkevičius</label>
<input class="chk" type="checkbox" name="mboxItemGIDs" value="S5935025294661423104_500" id="checkbox_S5935025294661423104_500">
<div class="date">
<span class="time-millis hidden">Mon Nov 03 13:11:37 UTC 2014</span>
<span class="today hidden">Today</span>
<span class="yesterday hidden">Yesterday</span>
<span class="this-year hidden">Nov 3</span>
<span class="past hidden">Nov 3, 2014</span>
</div>
<span class="participants">
<span class="to">To: </span>
Ina Bumstein
</span>
<div class="folder-subject">
<p class="subject">
<a class="detail-link " href="/inbox/#detail?itemId=S5935025294661423104_500&amp;trk=COMM_NI">
Join my network on LinkedIn
</a>
</p>
</div>
<p class="preview  not-empty">Laba diena,
Esu personalo atrankų konsultantas ir norėčiau Jus prisijungti prie savo profesionalų tinklo LinkedIn. Net jei šiuo metu ir...</p>
<span title="Star">
<a data-action="star" data-action-url="/inbox/action?mboxItemGID=S5935025294661423104_500&amp;actionType=star&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="flag-link" href="/inbox/action?mboxItemGID=S5935025294661423104_500&amp;actionType=star&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Star</a>
</span>
<span title="Unstar">
<a data-action="unstar" data-action-url="/inbox/action?mboxItemGID=S5935025294661423104_500&amp;actionType=unstar&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="unflag-link" href="/inbox/action?mboxItemGID=S5935025294661423104_500&amp;actionType=unstar&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Unstar</a>
</span>
<ul class="inbox-actions">
<li class="replyToSender">
<a href="/inbox/#msgToConns?itemID=S5935025294661423104_500&amp;displayReplyAll=" data-action-url="" data-action="replyAllMEBC">Reply</a>
</li>
<li class="forward">
<a data-action="forward" data-action-url="" class="" href="/inbox/#msgToConns?itemID=S5935025294661423104_500&amp;displayForward=&amp;trk=COMM_NI">Forward</a>
</li>
<li class="archive">
<a data-action="archive" data-action-url="/inbox/action?mboxItemGID=S5935025294661423104_500&amp;actionType=archive&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="" href="/inbox/action?mboxItemGID=S5935025294661423104_500&amp;actionType=archive&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Archive</a>
</li>
<li class="trash">
<a data-action="trash" data-action-url="/inbox/action?mboxItemGID=S5935025294661423104_500&amp;actionType=trash&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="" href="/inbox/action?mboxItemGID=S5935025294661423104_500&amp;actionType=trash&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Delete</a>
</li>
</ul>
</div>
</li>
<li data-gid="S5935023521351639041_500" class="inbox-item message-item subs-inbox-fac">
<img alt="Vytenis Butkevičius" class="photo" height="60" src="https://media.licdn.com/mpr/mpr/shrink_60_60/p/5/000/1d3/0ba/2517a91.jpg" width="60"/>
<div class="item-content actions-left">
<label for="checkbox_S5935023521351639041_500" class='hidden-accessible'>Vytenis Butkevičius</label>
<input class="chk" type="checkbox" name="mboxItemGIDs" value="S5935023521351639041_500" id="checkbox_S5935023521351639041_500">
<div class="date">
<span class="time-millis hidden">Mon Nov 03 13:04:34 UTC 2014</span>
<span class="today hidden">Today</span>
<span class="yesterday hidden">Yesterday</span>
<span class="this-year hidden">Nov 3</span>
<span class="past hidden">Nov 3, 2014</span>
</div>
<span class="participants">
<span class="to">To: </span>
Ernestas Žėkas
</span>
<span class="item-status item-status-accepted">
(Accepted)
</span>
<div class="folder-subject">
<p class="subject">
<a class="detail-link " href="/inbox/#detail?itemId=S5935023521351639041_500&amp;trk=COMM_NI">
Join my network on LinkedIn
</a>
</p>
</div>
<p class="preview  not-empty">Laba diena,
Esu personalo atrankų konsultantas ir norėčiau Jus prisijungti prie savo profesionalų tinklo LinkedIn. Net jei šiuo metu ir...</p>
<span title="Star">
<a data-action="star" data-action-url="/inbox/action?mboxItemGID=S5935023521351639041_500&amp;actionType=star&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="flag-link" href="/inbox/action?mboxItemGID=S5935023521351639041_500&amp;actionType=star&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Star</a>
</span>
<span title="Unstar">
<a data-action="unstar" data-action-url="/inbox/action?mboxItemGID=S5935023521351639041_500&amp;actionType=unstar&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="unflag-link" href="/inbox/action?mboxItemGID=S5935023521351639041_500&amp;actionType=unstar&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Unstar</a>
</span>
<ul class="inbox-actions">
<li class="replyToSender">
<a href="/inbox/#msgToConns?itemID=S5935023521351639041_500&amp;displayReplyAll=" data-action-url="" data-action="replyAllMEBC">Reply</a>
</li>
<li class="forward">
<a data-action="forward" data-action-url="" class="" href="/inbox/#msgToConns?itemID=S5935023521351639041_500&amp;displayForward=&amp;trk=COMM_NI">Forward</a>
</li>
<li class="archive">
<a data-action="archive" data-action-url="/inbox/action?mboxItemGID=S5935023521351639041_500&amp;actionType=archive&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="" href="/inbox/action?mboxItemGID=S5935023521351639041_500&amp;actionType=archive&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Archive</a>
</li>
<li class="trash">
<a data-action="trash" data-action-url="/inbox/action?mboxItemGID=S5935023521351639041_500&amp;actionType=trash&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="" href="/inbox/action?mboxItemGID=S5935023521351639041_500&amp;actionType=trash&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Delete</a>
</li>
</ul>
</div>
</li>
<li data-gid="S5935017481834889216_500" class="inbox-item message-item subs-inbox-fac">
<img src="https://static.licdn.com/scds/common/u/img/themes/katy/ghosts/profiles/ghost_profile_40x40_v1.png" class="photo" alt="Vytenis Butkevičius" height="60" width="60">
<div class="item-content actions-left">
<label for="checkbox_S5935017481834889216_500" class='hidden-accessible'>Vytenis Butkevičius</label>
<input class="chk" type="checkbox" name="mboxItemGIDs" value="S5935017481834889216_500" id="checkbox_S5935017481834889216_500">
<div class="date">
<span class="time-millis hidden">Mon Nov 03 12:40:34 UTC 2014</span>
<span class="today hidden">Today</span>
<span class="yesterday hidden">Yesterday</span>
<span class="this-year hidden">Nov 3</span>
<span class="past hidden">Nov 3, 2014</span>
</div>
<span class="participants">
<span class="to">To: </span>
Justas Skarzauskas
</span>
<div class="folder-subject">
<p class="subject">
<a class="detail-link " href="/inbox/#detail?itemId=S5935017481834889216_500&amp;trk=COMM_NI">
Join my network on LinkedIn
</a>
</p>
</div>
<p class="preview  not-empty">Laba diena,
Esu personalo atrankų konsultantas ir norėčiau Jus prisijungti prie savo profesionalų tinklo LinkedIn. Net jei šiuo metu ir...</p>
<span title="Star">
<a data-action="star" data-action-url="/inbox/action?mboxItemGID=S5935017481834889216_500&amp;actionType=star&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="flag-link" href="/inbox/action?mboxItemGID=S5935017481834889216_500&amp;actionType=star&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Star</a>
</span>
<span title="Unstar">
<a data-action="unstar" data-action-url="/inbox/action?mboxItemGID=S5935017481834889216_500&amp;actionType=unstar&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="unflag-link" href="/inbox/action?mboxItemGID=S5935017481834889216_500&amp;actionType=unstar&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Unstar</a>
</span>
<ul class="inbox-actions">
<li class="replyToSender">
<a href="/inbox/#msgToConns?itemID=S5935017481834889216_500&amp;displayReplyAll=" data-action-url="" data-action="replyAllMEBC">Reply</a>
</li>
<li class="forward">
<a data-action="forward" data-action-url="" class="" href="/inbox/#msgToConns?itemID=S5935017481834889216_500&amp;displayForward=&amp;trk=COMM_NI">Forward</a>
</li>
<li class="archive">
<a data-action="archive" data-action-url="/inbox/action?mboxItemGID=S5935017481834889216_500&amp;actionType=archive&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="" href="/inbox/action?mboxItemGID=S5935017481834889216_500&amp;actionType=archive&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Archive</a>
</li>
<li class="trash">
<a data-action="trash" data-action-url="/inbox/action?mboxItemGID=S5935017481834889216_500&amp;actionType=trash&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="" href="/inbox/action?mboxItemGID=S5935017481834889216_500&amp;actionType=trash&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Delete</a>
</li>
</ul>
</div>
</li>
<li data-gid="S5935017121028280322_500" class="inbox-item message-item subs-inbox-fac">
<img src="https://static.licdn.com/scds/common/u/img/themes/katy/ghosts/profiles/ghost_profile_40x40_v1.png" class="photo" alt="Vytenis Butkevičius" height="60" width="60">
<div class="item-content actions-left">
<label for="checkbox_S5935017121028280322_500" class='hidden-accessible'>Vytenis Butkevičius</label>
<input class="chk" type="checkbox" name="mboxItemGIDs" value="S5935017121028280322_500" id="checkbox_S5935017121028280322_500">
<div class="date">
<span class="time-millis hidden">Mon Nov 03 12:39:08 UTC 2014</span>
<span class="today hidden">Today</span>
<span class="yesterday hidden">Yesterday</span>
<span class="this-year hidden">Nov 3</span>
<span class="past hidden">Nov 3, 2014</span>
</div>
<span class="participants">
<span class="to">To: </span>
Gintautė Brazauskaitė
</span>
<span class="item-status item-status-accepted">
(Accepted)
</span>
<div class="folder-subject">
<p class="subject">
<a class="detail-link " href="/inbox/#detail?itemId=S5935017121028280322_500&amp;trk=COMM_NI">
Join my network on LinkedIn
</a>
</p>
</div>
<p class="preview  not-empty">Laba diena,
Esu personalo atrankų konsultantas ir norėčiau Jus prisijungti prie savo profesionalų tinklo LinkedIn. Net jei šiuo metu ir...</p>
<span title="Star">
<a data-action="star" data-action-url="/inbox/action?mboxItemGID=S5935017121028280322_500&amp;actionType=star&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="flag-link" href="/inbox/action?mboxItemGID=S5935017121028280322_500&amp;actionType=star&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Star</a>
</span>
<span title="Unstar">
<a data-action="unstar" data-action-url="/inbox/action?mboxItemGID=S5935017121028280322_500&amp;actionType=unstar&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="unflag-link" href="/inbox/action?mboxItemGID=S5935017121028280322_500&amp;actionType=unstar&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Unstar</a>
</span>
<ul class="inbox-actions">
<li class="replyToSender">
<a href="/inbox/#msgToConns?itemID=S5935017121028280322_500&amp;displayReplyAll=" data-action-url="" data-action="replyAllMEBC">Reply</a>
</li>
<li class="forward">
<a data-action="forward" data-action-url="" class="" href="/inbox/#msgToConns?itemID=S5935017121028280322_500&amp;displayForward=&amp;trk=COMM_NI">Forward</a>
</li>
<li class="archive">
<a data-action="archive" data-action-url="/inbox/action?mboxItemGID=S5935017121028280322_500&amp;actionType=archive&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="" href="/inbox/action?mboxItemGID=S5935017121028280322_500&amp;actionType=archive&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Archive</a>
</li>
<li class="trash">
<a data-action="trash" data-action-url="/inbox/action?mboxItemGID=S5935017121028280322_500&amp;actionType=trash&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="" href="/inbox/action?mboxItemGID=S5935017121028280322_500&amp;actionType=trash&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Delete</a>
</li>
</ul>
</div>
</li>
<li data-gid="S5935016690164203520_500" class="inbox-item message-item subs-inbox-fac">
<img alt="Vytenis Butkevičius" class="photo" height="60" src="https://media.licdn.com/mpr/mpr/shrink_60_60/p/6/005/019/089/1e022b6.jpg" width="60"/>
<div class="item-content actions-left">
<label for="checkbox_S5935016690164203520_500" class='hidden-accessible'>Vytenis Butkevičius</label>
<input class="chk" type="checkbox" name="mboxItemGIDs" value="S5935016690164203520_500" id="checkbox_S5935016690164203520_500">
<div class="date">
<span class="time-millis hidden">Mon Nov 03 12:37:26 UTC 2014</span>
<span class="today hidden">Today</span>
<span class="yesterday hidden">Yesterday</span>
<span class="this-year hidden">Nov 3</span>
<span class="past hidden">Nov 3, 2014</span>
</div>
<span class="participants">
<span class="to">To: </span>
Edmundas Vitėnas
</span>
<span class="item-status item-status-accepted">
(Accepted)
</span>
<div class="folder-subject">
<p class="subject">
<a class="detail-link " href="/inbox/#detail?itemId=S5935016690164203520_500&amp;trk=COMM_NI">
Join my network on LinkedIn
</a>
</p>
</div>
<p class="preview  not-empty">Laba diena,
Esu personalo atrankų konsultantas ir norėčiau Jus prisijungti prie savo profesionalų tinklo LinkedIn. Net jei šiuo metu ir...</p>
<span title="Star">
<a data-action="star" data-action-url="/inbox/action?mboxItemGID=S5935016690164203520_500&amp;actionType=star&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="flag-link" href="/inbox/action?mboxItemGID=S5935016690164203520_500&amp;actionType=star&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Star</a>
</span>
<span title="Unstar">
<a data-action="unstar" data-action-url="/inbox/action?mboxItemGID=S5935016690164203520_500&amp;actionType=unstar&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="unflag-link" href="/inbox/action?mboxItemGID=S5935016690164203520_500&amp;actionType=unstar&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Unstar</a>
</span>
<ul class="inbox-actions">
<li class="replyToSender">
<a href="/inbox/#msgToConns?itemID=S5935016690164203520_500&amp;displayReplyAll=" data-action-url="" data-action="replyAllMEBC">Reply</a>
</li>
<li class="forward">
<a data-action="forward" data-action-url="" class="" href="/inbox/#msgToConns?itemID=S5935016690164203520_500&amp;displayForward=&amp;trk=COMM_NI">Forward</a>
</li>
<li class="archive">
<a data-action="archive" data-action-url="/inbox/action?mboxItemGID=S5935016690164203520_500&amp;actionType=archive&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="" href="/inbox/action?mboxItemGID=S5935016690164203520_500&amp;actionType=archive&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Archive</a>
</li>
<li class="trash">
<a data-action="trash" data-action-url="/inbox/action?mboxItemGID=S5935016690164203520_500&amp;actionType=trash&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI" class="" href="/inbox/action?mboxItemGID=S5935016690164203520_500&amp;actionType=trash&amp;csrfToken=ajax%3A7352798163445213269&amp;trk=COMM_NI">Delete</a>
</li>
</ul>
</div>
</li>
</ol>
<div class="inbox-null-msg">
<p class="null-default">There are no sent messages.</p>
<p class="null-unread hidden">There are no unread messages.</p>
<p class="null-flagged hidden">There are no starred messages.</p>
<p class="null-inmail hidden">There are no InMails.</p>
<p class="null-recommendations hidden">There are no recommendation messages.</p>
<p class="null-intros hidden">There are no introduction messages.</p>
<p class="null-profiles hidden">There are no profile messages.</p>
<p class="null-jobs hidden">There are no job messages.</p>
<p class="null-blocked hidden">There are no blocked messages.</p>
</div>
<div class="pageIndex">
<ul>
<li class="first">
<a class="inactive">
First
</a>
</li>
<li class="prev">
<a class="inactive">
Previous
</a>
</li>
<li class="page">
Page 1 of 112
</li>
<li class="next">
<span class="hover-tooltip">
<a href="/inbox/#sent?startRow=11&amp;subFilter=&amp;keywords=&amp;sortBy=">
Next
</a>
</span>
</li>
<li class="last">
<span class="hover-tooltip">
<a href="/inbox/#sent?startRow=1111&amp;subFilter=&amp;keywords=&amp;sortBy=">
Last
</a>
</span>
</li>
</ul>
</div>
<input type="hidden" name="mboxItemGIDs" value="" id="mboxItemGIDs-bulkActionForm"><input type="hidden" name="csrfToken" value="ajax:7352798163445213269" id="csrfToken-bulkActionForm"><input type="hidden" name="sourceAlias" value="0_2x0gd9V7U0btrbyLwJ1Mmi" id="sourceAlias-bulkActionForm">
</form>
</div>
</div>
</div>
</div>
</div>
"""

soup = BeautifulSoup(page).find_all('li', class_=re.compile("inbox-item"))
print(len(soup))