from flask import render_template,request,Blueprint,url_for,flash, redirect
from program.flow_search.forms import SearchForm

from program.flow_search import song_data

flow_search = Blueprint('flow_search',__name__)

@flow_search.route('/',methods=['GET','POST'])
def search():
    form = SearchForm()
    artist_got_from_form = request.form.get('search_artist')
    artist = song_data.get_artist_name(str(artist_got_from_form))
    artist_without_blank = artist.replace(' ','&')
    if form.validate_on_submit():
        return redirect(url_for('flow_search.result',artist_without_blank=artist_without_blank))
    
    return render_template('/flow_search.html',form=form)


@flow_search.route('/search-result/<artist_without_blank>')
def result(artist_without_blank):
    artist_in_url = artist_without_blank.replace('&&',' ')
    artist = song_data.get_artist_name(str(artist_in_url))
    genre = request.form.get('search_genre')
    artist_image = song_data.get_artist_image(artist)
    track_data = song_data.show_results(artist)
    artist_popularity = song_data.get_artist_popularity(artist)
    labels = song_data.get_artist_copytights(artist)
    packs = song_data.sample_packs_recommend(artist)
    length = len(packs)
    chordify_url = song_data.get_chord_progressions(artist)
    video_ids = song_data.youtube_tutorials(artist)
    return render_template('/search_result.html',artist=artist,genre=genre,
    track_data=track_data,artist_image=artist_image,
    artist_popularity=artist_popularity,labels=labels,packs=packs,length=length,
    chordify_url=chordify_url,video_ids=video_ids)