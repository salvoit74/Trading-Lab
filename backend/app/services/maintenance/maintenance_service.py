import logging

import psycopg2

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from services.maintenance.task_registry import TASKS


logger = logging.getLogger(__name__)


class MaintenanceService:

    def __init__(self):

        self.last_check = None


    def run(self):

        #
        # controlla al massimo una volta ogni ora
        #

        now = datetime.now(
            ZoneInfo("UTC")
        )

        if (
            self.last_check is not None
            and
            now < self.last_check + timedelta(hours=1)
        ):
            return

        self.last_check = now

        self.execute_tasks()


    def execute_tasks(self):

        import os

        conn = psycopg2.connect(
            host=os.environ["DB_HOST"],
            database=os.environ["APP_DB"],
            user=os.environ["APP_USER"],
            password=os.environ["APP_PASSWORD"]
        )

        cur = conn.cursor()

        cur.execute("""
            SELECT
                task_name,
                interval_seconds,
                last_execution
            FROM maintenance_tasks
            WHERE enabled = TRUE
            ORDER BY task_name
        """)

        tasks = cur.fetchall()

        for (
            task_name,
            interval_seconds,
            last_execution
        ) in tasks:

            if task_name not in TASKS:

                logger.warning(
                    "Unknown maintenance task %s",
                    task_name
                )

                continue


            execute = False

            if last_execution is None:

                execute = True

            else:

                elapsed = (
                    datetime.now(
                        ZoneInfo("UTC")
                    ) - last_execution
                ).total_seconds()

                execute = elapsed >= interval_seconds


            if not execute:

                continue


            logger.info(
                "Running maintenance task %s",
                task_name
            )


            TASKS[task_name]()


            cur.execute("""
                UPDATE maintenance_tasks
                   SET last_execution = %s
                 WHERE task_name = %s
            """,
            (
                datetime.now(
                    ZoneInfo("UTC")
                ),
                task_name
            ))

            conn.commit()


        cur.close()
        conn.close()
