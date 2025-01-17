from pathlib import Path
import logging
import argparse
from datetime import datetime
from typing import Dict, Any
import urllib.request
import pandas as pd
from sqlalchemy import create_engine, Engine
from sqlalchemy.exc import SQLAlchemyError

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseLoader:
    def __init__(self, connection_params: Dict[str, Any]):
        """
        Initialize loader with connection parameters
        """
        self.params = connection_params
        self.engine = self._create_engine()
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)

    def _create_engine(self) -> Engine:
        """
        Create SQLAlchemy engine with error handling
        """
        try:
            return create_engine(
                f'postgresql://{self.params["user"]}:{self.params["password"]}'
                f'@{self.params["host"]}:{self.params["port"]}/{self.params["db"]}'
            )
        except Exception as e:
            logger.error(f"Error creating engine: {str(e)}")
            raise

    def _download_file(self, url: str, output_path: Path) -> None:
        """
        Download file with progress tracking
        """
        try:
            logger.info(f"Downloading file from {url}")
            urllib.request.urlretrieve(url, output_path)
            logger.info("Download completed")
        except Exception as e:
            logger.error(f"Download error: {str(e)}")
            raise

    def ingest_data(self, url: str, table_name: str, chunk_size: int = 100_000) -> None:
        """
        Ingest data from CSV to PostgreSQL with progress tracking
        """
        output_path = Path('data/output.csv.gz' if url.endswith('.csv.gz') else 'data/output.csv')
        
        try:
            self._download_file(url, output_path)

            logger.info("Counting chunks...")
            total_chunks = sum(1 for _ in pd.read_csv(output_path, iterator=True, chunksize=chunk_size))

            chunks = pd.read_csv(output_path, iterator=True, chunksize=chunk_size)
            
            # Table preparation
            first_chunk = next(chunks)
            
            # Criar tabela sem índices
            first_chunk.head(0).to_sql(
                name=table_name, 
                con=self.engine, 
                if_exists='replace'
            )
            
            # Inserir primeiro chunk
            self._insert_chunk(first_chunk, table_name, 1, total_chunks)
            
            # Inserir chunks restantes
            for i, chunk in enumerate(chunks, start=2):
                self._insert_chunk(chunk, table_name, i, total_chunks)

        except Exception as e:
            logger.error(f"Error: {str(e)}")
            raise
        finally:
            if output_path.exists():
                output_path.unlink()

    def _insert_chunk(self, df: pd.DataFrame, table_name: str, current: int = 0, total: int = 0) -> None:
        """
        Insert a chunk into database with time measurement
        """
        start_time = datetime.now()
        try:
            df.to_sql(
                name=table_name,
                con=self.engine,
                if_exists='append'
            )
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"Chunk {current}/{total} inserted in {duration:.2f}s")
        except SQLAlchemyError as e:
            logger.error(f"Error inserting chunk: {str(e)}")
            raise

def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description='Ingest CSV data to PostgreSQL')
    parser.add_argument('--user', required=True, help='PostgreSQL user')
    parser.add_argument('--password', required=True, help='PostgreSQL password')
    parser.add_argument('--host', required=True, help='PostgreSQL host')
    parser.add_argument('--port', required=True, help='PostgreSQL port')
    parser.add_argument('--db', required=True, help='Database name')
    parser.add_argument('--table_name', required=True, help='Target table name')
    parser.add_argument('--url', required=True, help='CSV file URL')
    parser.add_argument('--chunk_size', type=int, default=100_000, help='Chunk size')
    
    return parser.parse_args()

def main() -> None:
    """
    Main function
    """
    args = parse_args()
    
    connection_params = {
        'user': args.user,
        'password': args.password,
        'host': args.host,
        'port': args.port,
        'db': args.db
    }

    try:
        loader = DatabaseLoader(connection_params)
        loader.ingest_data(args.url, args.table_name, args.chunk_size)
        logger.info("Ingestion completed successfully!")
    except Exception as e:
        logger.error(f"Execution error: {str(e)}")
        raise

if __name__ == '__main__':
    main()