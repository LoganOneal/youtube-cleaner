# youtube-cleaner

A web service to help re-monetize your content! Upload a video or get one from Youtube, and ban certain words from being said in your video.

## team members

Sarah Huang
Mikolaj Jakowski
Logan Oneal
Zavier Miller

## shouts

Big thanks to the VolHacks board and all the sponsors/mentors. It was a super fun experience!!

## getting started

Our project uses Docker so just clone the repo, run `make` and connect to `localhost:5000` to get using locally.

## structure

### `app`

The main Flask app directory

### `events`

Server sent events

### `extensions`

Abstractions to certain APIs to keep the code clean

### `jobs`

Background jobs that get run by the worker thread

### `routes`

The routes and views for the app
