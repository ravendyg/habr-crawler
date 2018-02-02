# Habr crawler

A tool previously written in R, reborn again.

## Dependencies
A quick and dirty prototype. Wants everything installed globaly. Just run and see wether there is smth missing.

## Configuration
* work_dir - path to a directory where output and settings a stored
* urls - list of base urls, currently habrahabr and geektimes
* count - max numer of articles. Crawler will collect articles until the one found befoer is met or count limit is reached. Whatever happens first. Hardcoded top limit is 500. If you need more then smth went wrong or you know what you are doing and can hack around to make it work.

## First run
Provide `stop_id` file in the `work_dir` (it's a csv [`url`, `stop_id`]) or specify count. Or just let it load the last 500 articles. After that it will remember the last article id and will load only the new ones (given you haven't deleted `stop_id` file).

## TODO
* Fix dependencies, currently in searches for everything globaly;
* Some refactoring, everything is in a one file now;
* Add markers for the authors I'd definitely like or don't like to read (like in R version).

### Also
Check out my cool Chrome [habrahabr extension](https://github.com/ravendyg/habr-collapse) ))
