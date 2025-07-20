New features:
- [x] Title/Welcome Screen
- [x] change url /new to /<song_id>
- [x] If that song_id does not exist, redirect to main page
- [ ] Extract from YouTube link
- [x] Colorize the waveform links
- [x] Volume for every track
- [x] Master volume
- [x] Option to download individual stems
- [x] Option to download all the stems
- [x] Option to change the file format (mp3/fac/wav)
- [x] move timeline to top
- [ ] Detect BPM and display it
- [x] Zoom ?
- [x] Redirect to new configuration after dragging file onto player

Bug fixes:
- [x] After track finished playing, user should be able to use space to restart
- [x] After pressing an element and pressing space, it should not reactivate the element
- [x] Timeline suddenly disappeared, the container is there tho
- [x] If the song_id does not exist it should return 404, not 500
- [ ] Selecting an output format doesn't work, API returns WAV everytime.

Nice to have:
- [ ] a "master track" that has all the stems together