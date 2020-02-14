FROM 339570402237.dkr.ecr.eu-west-1.amazonaws.com/company/astrosat/base:python36-node10

USER app

ENV PIPENV_VENV_IN_PROJECT=1
ENV PIPENV_DONT_LOAD_ENV=1

WORKDIR $APP_HOME

# Install server deps
# Note that we copy Pipfile from the server directory to the root directory.
# This ensures the venv is not overwritten by the volume mounted in docker-compose.
# Note that we also copy setup.py and astrosat_tasks so that pipenv can find editable dependencies
# (and I don't care if those get overwritten)
# COPY --chown=app:app ./example/Pipfile* $APP_HOME/
# COPY --chown=app:app ./setup.py ./astrosat_tasks/ $APP_HOME/
COPY --chown=app:app . $APP_HOME/
RUN cd $APP_HOME && pipenv install --dev

# Install server code
# COPY --chown=app:app . $APP_HOME/example

# Start task queue
# COPY --chown=root:root run-celery.sh /etc/service/celery/run

# Start dev server
COPY --chown=root:root run-server.sh /etc/service/server/run

# necessary to have permission to remove nginx support
USER root
RUN rm -rf /etc/service/nginx

# The baseimage requires ultimately running as root
USER root
