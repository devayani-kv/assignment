# assignment
How to run the project:
1) you will need to get an openai API key and a weather API key (get your weather API key from this website: https://www.weatherapi.com/)
2) Set the value of the API keys in the .env file before anything
3) The audio clip is already present, but feel free to load an audio of your choice. You will have to change the path to the audio in the audio_extract file
4) Run audio_extract.py first to transcribe the audio
5) Then run setup_database.py to setup the vector database and push the transcribed text in
6) Then run main.py

## List of deliverables
1) Explanation of the files
   - audio_extract: transcribes the text using whisper API and saves it in 'transcription_text1'
   - extract_country: extracts the place mentioned in the text
   - setup_database: sets up the vector database and pushes the transcribed text into the database
   - weather: extracts the info about the weather in a specific place using the weather API
   - wikipedia: extracts info about the place using the wikipedia API
2) Audio File: audio.mp3 is the recording used for the project
3) Transcription Output: transcription_text1.txt is the transcribed output of the audio
4) Wikipedia and Weather results:
   - city.json: contains the place extracted from the audio
   - description.txt: contains the Wikipedia results
   - weather_info.json: contains the weather parameters for the place
