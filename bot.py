from __future__ import print_function
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
                         CallbackQueryHandler, ConversationHandler, CallbackContext
from pprint import pprint
from commands import help_command, trivia_command, hungry_command, joke_command, \
                     substitute, update_rating
from general_helpers import start
from threading import Thread

import os
import logging
import json
import sys

