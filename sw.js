// Lets the app install and open offline: see https://github.com/petravanta/general/blob/main/STANDARDS.md#installing-on-a-phone
self.APP_SHELL = ["./", "manifest.webmanifest", "icon-192.png", "icon.svg", "data/sets.json", "data/sets/us-civics-2008.json", "data/sets/wa-motorcycle-2w.json", "data/sets/wa-motorcycle-3w.json"];
importScripts('https://petravanta.github.io/general/shared/app-sw.js');
