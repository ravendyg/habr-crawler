# Habr crawler

A tool previously written in R, reborn again.

## Dependencies
A quick and dirty prototype. Wants everything installed globaly. Just run and see wether there is smth missing.

## Configuration
* work_dir - path to a directory where output and settings a stored
* urls - list of base urls, currently habrahabr and geektimes
* offset? - how many days before today you want to load (unless `last_run` has been provided), default - 7 days
UTC time is used and habr dates are treated as such. It's wrong but consistent and easier that to figure out in what timezone the script has been ran. And I need this consistency since running the parser from different timezones.

## TODO
* Fix dependencies, currently in searches for everything globaly;
* Some refactoring, everything is in a one file now;
* Add markers for the authors I'd definitely like or don't like to read (like in R version).

### Also
Check out my cool Chrome [habrahabr extension](https://github.com/ravendyg/habr-collapse) ))
