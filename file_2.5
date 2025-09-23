#!/usr/bin/env python3
"""
zimbra_spam_cleaner.py
اتصال به Zimbra (IMAP)، بررسی ایمیل‌ها و تشخیص اسپم/هَم با استفاده از کتابخانه متن‌باز spam-detector.
اسپم‌ها به پوشه Trash منتقل می‌شوند (یا در حالت dry-run فقط گزارش می‌شوند).

Usage example:
  python zimbra_spam_cleaner.py --host mail.example.com --user you@example.com --password secret \
    --mailbox INBOX --dry-run
"""

import imaplib
import email
from email.header import decode_header
import argparse
import logging
import re
import sys

# کتابخانه متن‌باز اسپم
from spam_detector.detector import SpamDetector

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

# ---------------------------
# اتصال به IMAP
# ---------------------------
def connect_imap(host: str, port: int, user: str, password: str, use_ssl: bool = True):
    logging.info(f"Connecting to IMAP {host}:{port} SSL={use_ssl} as {user}")
    if use_ssl:
        M = imaplib.IMAP4_SSL(host, port)
    else:
        M = imaplib.IMAP4(host, port)
    M.login(user, password)
    return M

# ---------------------------
# کمکی‌ها
# ---------------------------
def decode_mime_words(s):
    if not s:
        return ""
    parts = decode_header(s)
    out = []
    for part, enc in parts:
        if isinstance(part, bytes):
            try:
                out.append(part.decode(enc or "utf-8", errors="ignore"))
            except Exception:
                out.append(part.decode("latin1", errors="ignore"))
        else:
            out.append(part)
    return "".join(out)

def extract_text_from_message(msg: email.message.Message) -> str:
    texts = []
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = str(part.get("Content-Disposition") or "")
            if ctype == "text/plain" and "attachment" not in disp:
                try:
                    payload = part.get_payload(decode=True)
                    texts.append(payload.decode(part.get_content_charset() or "utf-8", errors="ignore"))
                except Exception:
                    texts.append(str(part.get_payload(decode=True)))
    else:
        try:
            payload = msg.get_payload(decode=True)
            texts.append(payload.decode(msg.get_content_charset() or "utf-8", errors="ignore"))
        except Exception:
            texts.append(str(msg.get_payload(decode=True)))
    return "\n".join(t for t in texts if t).strip()

def ensure_trash_folder(M: imaplib.IMAP4, trash_name: str = "Trash") -> str:
    for name in [trash_name, "INBOX.Trash", "Deleted Items", "INBOX/Trash"]:
        typ, data = M.list('""', name)
        if typ == "OK" and data and data[0]:
            return name
    try:
        M.create(trash_name)
        return trash_name
    except Exception:
        return trash_name

# ---------------------------
# پردازش ایمیل‌ها
# ---------------------------
def process_mailbox(M: imaplib.IMAP4, mailbox: str, dry_run: bool = True, limit=None):
    logging.info(f"Selecting mailbox {mailbox}")
    typ, _ = M.select(f'"{mailbox}"')
    if typ != "OK":
        raise RuntimeError(f"Failed to select mailbox {mailbox}: {typ}")

    typ, data = M.search(None, "ALL")
    if typ != "OK":
        logging.error("Search failed")
        return
    uids = data[0].split()
    logging.info(f"Found {len(uids)} messages in {mailbox}")

    detector = SpamDetector()
    trash_folder = ensure_trash_folder(M)

    processed = 0
    for i, uid in enumerate(reversed(uids)):  # newest first
        if limit and processed >= limit:
            break
        try:
            typ, msg_data = M.fetch(uid, "(RFC822)")
            if typ != "OK":
                logging.warning(f"Failed to fetch UID {uid}")
                continue
            raw = msg_data[0][1]
            msg = email.message_from_bytes(raw)
            subject = decode_mime_words(msg.get("Subject"))
            body = extract_text_from_message(msg)

            text = (subject or "") + " " + (body or "")
            is_spam = detector.is_spam(text)

            logging.info(f"UID {uid.decode() if isinstance(uid, bytes) else uid}: "
                         f"Subject='{subject[:60]}' => spam={is_spam}")

            if is_spam:
                if dry_run:
                    logging.info(f"[DRY-RUN] Would move UID {uid} to {trash_folder}")
                else:
                    typc, _ = M.uid("COPY", uid, trash_folder)
                    if typc != "OK":
                        logging.warning(f"Failed to copy UID {uid} to {trash_folder}")
                    else:
                        M.uid("STORE", uid, "+FLAGS", r"(\Deleted)")
        except Exception as e:
            logging.exception(f"Error processing UID {uid}: {e}")
        processed += 1

    if not dry_run:
        logging.info("Expunging mailbox to finalize deletions")
        M.expunge()

# ---------------------------
# main
# ---------------------------
def main():
    parser = argparse.ArgumentParser(description="Zimbra spam cleaner (spam-detector edition)")
    parser.add_argument("--host", required=True, help="IMAP host")
    parser.add_argument("--port", type=int, default=993, help="IMAP port (default 993 for SSL)")
    parser.add_argument("--user", required=True, help="IMAP username")
    parser.add_argument("--password", required=True, help="IMAP password")
    parser.add_argument("--mailbox", default="INBOX", help="Mailbox to scan (default INBOX)")
    parser.add_argument("--dry-run", action="store_true", help="Do not delete/move messages; just report")
    parser.add_argument("--limit", type=int, help="Limit number of messages to process")
    parser.add_argument("--no-ssl", action="store_true", help="Disable SSL")
    args = parser.parse_args()

    M = connect_imap(args.host, args.port, args.user, args.password, use_ssl=not args.no_ssl)
    try:
        process_mailbox(M, args.mailbox, dry_run=args.dry_run, limit=args.limit)
    finally:
        logging.info("Logging out")
        try:
            M.logout()
        except Exception:
            pass

if __name__ == "__main__":
    main()


#توجه!  برای ران کردن از دستور زیر به صورت جداگانه استفاده کنید:
'''python zimbra_spam_cleaner.py \
  --host mail.example.com --user you@example.com --password secret \
  --mailbox INBOX --dry-run'''
