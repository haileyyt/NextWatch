# NextWatch

An open-source recommendation project designed to help users discover their next favorite show.

## About the project

Choosing what to watch can take longer than expected, even when there are plenty of options. NextWatch will explore how genre preferences, explicit likes and dislikes, and viewing behavior can help generate more personalized show recommendations.

The initial use case is helping users discover shows to watch on Netflix. The long-term goal is to pair a recommendation engine with a clean, intuitive interface that makes finding something new simple and enjoyable.

I am developing this project as part of the Cline Campus Ambassador Program at Carnegie Mellon University and plan to use Cline throughout the development process.

## Current status

NextWatch is currently in the planning stage. This repository documents the initial scope, proposed technical approach, and development roadmap.

A working application, recommendation model, and streaming-service integrations have not been implemented yet.

## Planned features

### Initial version

- Collect favorite genres and explicitly liked or disliked shows.
- Generate a short, personalized list of show recommendations.
- Exclude explicitly disliked and already-watched titles from discovery results.
- Provide brief explanations of why each show was recommended.
- Present results through a simple interface.

### Future experiments

- Explore whether self-reported rewatch preferences improve recommendations.
- Allow users to provide feedback on suggested shows.
- Investigate optional imports of user-provided viewing history.
- Explore whether voluntarily shared YouTube interests provide useful additional signals.

YouTube integration is a stretch goal and will not be required to use the initial version.

## Proposed technical approach

The first prototype will use Python, with a simple interface tentatively built using Streamlit.

Development will begin with a genre-based recommendation baseline. I then plan to explore TF-IDF representations of show descriptions and cosine similarity to identify relevant titles.

More complex methods will be considered after evaluating the initial approach. The technical stack and feature set may change as the project develops.

## Data and privacy

The initial version will use manually entered preferences and a small catalog with documented sources and reuse permissions.

The project will not require users to provide Netflix or YouTube login credentials. Personal viewing histories, API keys, and other private information should never be committed to this repository.

Any future history-import feature will require a separate review of supported formats, user consent, and data handling.

Netflix availability has not been verified. Future availability information should identify the relevant region and verification date.

## Development roadmap

See [docs/project-plan.md](docs/project-plan.md) for the planned milestones and scope.

## Contributing

Feedback on recommendation signals, interface design, evaluation, and suitable data sources is welcome.

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

Original project code and documentation are available under the [MIT License](LICENSE). Third-party datasets and assets remain subject to their own licenses.

## Disclaimer

NextWatch is an independent student project and is not affiliated with Netflix or YouTube.