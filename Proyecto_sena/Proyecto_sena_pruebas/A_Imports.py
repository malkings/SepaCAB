#A_Imports contiene todos los imports a utilizar en el backend
#del proyecto SEPA CAB WEB APRENDICES

from flask import  Flask, redirect, render_template, request, session
from flask import send_from_directory
import mysql.connector
import os
from datetime import timedelta, datetime

import tkinter as tk
