#A_Imports contiene todos los imports a utilizar en el backend
#del proyecto SEPA CAB WEB APRENDICES

from flask import  Flask, redirect, render_template, request, session
from flask import send_from_directory
from flask import url_for
##from cryptography.fernet import Fernet
import mysql.connector
import os, hashlib, re, random, secrets
from datetime import timedelta, datetime

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


import string
