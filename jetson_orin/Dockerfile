FROM nvcr.io/nvidia/l4t-base:35.4.1

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt update -y && apt upgrade -y && apt install -y --no-install-recommends \
	pkg-config \
	libcairo2-dev \
	libgirepository1.0-dev \
	libffi-dev \
	libmount-dev \
	ninja-build \
	meson \
	libcairo2-dev \
	libglib2.0-dev \
	gcc \
	python3-gi \
	python3-gi-cairo \
	python3-dev \
	python3-pip 

RUN apt install -y --no-install-recommends gstreamer1.0-tools gstreamer1.0-alsa \
	gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
	gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
	gstreamer1.0-libav

RUN apt install -y --no-install-recommends libgstreamer1.0-dev \
	libgstreamer-plugins-base1.0-dev \
	libgstreamer-plugins-bad1.0-dev \
	libgstreamer-plugins-good1.0-dev

RUN python3 -m pip install -U pip setuptools

COPY requirements.txt requirements.txt

RUN python3 -m pip install --ignore-installed -r requirements.txt

COPY main.py /app

ENV CAMERA_ID 0
ENV MICROPHONE_ID 0,0
ENV PORTNUMBER 8000

EXPOSE 8000

CMD ["python3", "main.py"]
